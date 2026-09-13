import { mkdir, readdir, readFile, rm, writeFile } from 'node:fs/promises';
import { dirname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const requiredFields = ['item_id', 'title', 'date', 'source_url', 'summary'];
const scriptDirectory = fileURLToPath(new URL('.', import.meta.url));
const projectRoot = join(scriptDirectory, '..');
const postsDirectory = join(projectRoot, 'site', 'posts');
const indexPath = join(postsDirectory, 'index.md');
const tagsDirectory = join(projectRoot, 'site', 'tags');
const tagsPath = join(tagsDirectory, 'index.md');
const recentDirectory = join(projectRoot, 'site', 'recent');
const recentPath = join(recentDirectory, 'index.md');
const podcastsDirectory = join(projectRoot, 'site', 'podcasts');
const podcastsIndexPath = join(podcastsDirectory, 'index.md');
const homePath = join(projectRoot, 'site', 'index.md');
const sidebarDataPath = join(projectRoot, 'site', '.vitepress', 'sidebar.data.json');
const postsOrderPath = join(projectRoot, 'site', '.vitepress', 'posts-order.json');
const dataDirectory = join(projectRoot, 'data', 'items');
const collectedAtPath = join(projectRoot, 'data', 'collected-at.json');
const publicDirectory = join(projectRoot, 'site', 'public');
const siteBase = '/EchoForge/';

const sourceDescriptions = {
  'data-skeptic': '关注数据科学、机器学习与推荐系统的研究脉络，也经常追问技术如何影响真实用户。',
  'latent-space': '面向 AI 研究与工程实践的访谈，覆盖基础模型、科学计算与前沿研究者的工作方法。',
  'practical-ai': '讨论人工智能如何进入产品、组织与工程流程，重视落地条件和实际边界。',
  recsperts: '聚焦推荐系统研究、工业实践与学术讨论的技术播客。',
  'software-engineering-daily': '面向软件工程师的深度访谈，覆盖系统、工具、架构与开发者实践。'
};

function parseFrontmatter(source, filePath) {
  const match = source.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);

  if (!match) {
    throw new Error(`${relative(projectRoot, filePath)} must start with YAML frontmatter.`);
  }

  const fields = new Map();

  for (const line of match[1].split(/\r?\n/)) {
    if (!line.trim() || line.trimStart().startsWith('#')) {
      continue;
    }

    const separator = line.indexOf(':');
    if (separator === -1) {
      throw new Error(`${relative(projectRoot, filePath)} has invalid frontmatter line: ${line}`);
    }

    const key = line.slice(0, separator).trim();
    let value = line.slice(separator + 1).trim();

    if (!key || !value) {
      throw new Error(`${relative(projectRoot, filePath)} requires a value for every frontmatter field.`);
    }

    if ((value.startsWith("'") && value.endsWith("'")) || (value.startsWith('"') && value.endsWith('"'))) {
      value = value.slice(1, -1);
    }

    if (fields.has(key)) {
      throw new Error(`${relative(projectRoot, filePath)} repeats frontmatter field: ${key}`);
    }

    fields.set(key, value);
  }

  for (const field of requiredFields) {
    if (!fields.get(field)) {
      throw new Error(`${relative(projectRoot, filePath)} is missing required frontmatter field: ${field}`);
    }
  }

  const date = fields.get('date');
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || Number.isNaN(Date.parse(`${date}T00:00:00Z`))) {
    throw new Error(`${relative(projectRoot, filePath)} has invalid date: ${date}`);
  }

  try {
    const sourceUrl = new URL(fields.get('source_url'));
    if (!['http:', 'https:'].includes(sourceUrl.protocol)) {
      throw new Error('unsupported protocol');
    }
  } catch {
    throw new Error(`${relative(projectRoot, filePath)} has invalid source_url: ${fields.get('source_url')}`);
  }

  return Object.fromEntries(fields);
}

function parseTags(value) {
  if (!value) {
    return [];
  }
  const inner = value.trim().replace(/^\[/, '').replace(/\]$/, '');
  return inner
    .split(',')
    .map((tag) => tag.trim().replace(/^['"]/, '').replace(/['"]$/, ''))
    .filter(Boolean);
}

function escapeMarkdown(text) {
  return text.replace(/([\\[\]])/g, '\\$1');
}

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function yamlQuote(value) {
  return `'${String(value).replace(/'/g, "''")}'`;
}

function tagHref(tag) {
  return encodeURIComponent(tag).replace(/%2F/gi, '') + '/';
}

function readingMinutes(article) {
  const match = String(article.reading_minutes ?? '').match(/^\d+$/);
  return match ? Number(match[0]) : 1;
}

function articleTags(article, separator = ' / ') {
  return article.tags.map((tag) => `[${escapeMarkdown(tag)}](/tags/${tagHref(tag)})`).join(separator);
}

function articleLink(article, linkPrefix) {
  const lines = [
    `- [${escapeMarkdown(article.title)}](${linkPrefix}${article.path})`,
    `  - ${escapeMarkdown(article.summary)}`,
    `  - ${escapeMarkdown(article.source_name ?? article.source_url)} · 阅读约 ${readingMinutes(article)} 分钟 · ${articleTags(article)}`,
    `  - 节目发布：${article.published_at ?? '日期未知'} · 整理：${article.date}`
  ];
  return lines.join('\n');
}

function localDateString(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function buildRecentPage(articles) {
  const recent = articles.filter((candidate) => candidate.input_type !== 'demo').slice(0, 5);
  const entries = recent.length
    ? recent
        .map((article) =>
          [
            `### [${escapeMarkdown(article.title)}](/posts/${article.path})`,
            '',
            escapeMarkdown(article.summary),
            '',
            `${escapeMarkdown(article.source_name ?? article.source_url)} · 阅读约 ${readingMinutes(article)} 分钟 · ${articleTags(article)}`,
            '',
            `节目发布：${article.published_at ?? '日期未知'} · 整理：${article.date}`
          ].join('\n')
        )
        .join('\n\n')
    : '> 还没有可发布的文章。';
  return `---\nlayout: doc
pageClass: article-list\ntitle: 最近整理\nprev: false\nnext: false\n---\n\n# 最近整理\n\n最新整理的中文技术播客笔记：一句话摘要、节目来源、阅读时长和主题标签，帮助快速判断哪些值得细读。\n\n${entries}\n\n[查看全部文章 →](/posts/)\n`;
}

function buildAllArticlesPage(articles) {
  const byYear = new Map();
  for (const article of articles.filter((candidate) => candidate.input_type !== 'demo')) {
    const year = article.date.slice(0, 4);
    if (!byYear.has(year)) {
      byYear.set(year, []);
    }
    byYear.get(year).push(article);
  }

  const sections = [...byYear.keys()]
    .sort((left, right) => right.localeCompare(left))
    .map(
      (year) =>
        `## ${year}\n\n${byYear.get(year).map((article) => articleLink(article, './')).join('\n')}`
    )
    .join('\n\n');

  const body = sections || '> 还没有可发布的文章。';
  return `---\nlayout: doc
pageClass: article-list\ntitle: 全部文章\nprev: false\nnext: false\n---\n\n# 全部文章\n\nEchoForge 已发布的中文技术播客笔记，按整理年份分组，年份内按整理日期倒序。每篇文章都提供一句话摘要、节目来源、阅读时长和主题标签。\n\n${body}\n`;
}

async function loadItems() {
  const entries = await readdir(dataDirectory, { withFileTypes: true, recursive: true });
  const items = [];
  for (const entry of entries) {
    if (!entry.isFile() || !entry.name.endsWith('.json')) {
      continue;
    }
    try {
      items.push(JSON.parse(await readFile(join(entry.parentPath, entry.name), 'utf8')));
    } catch {
      // malformed metadata is reported by content-check; stats just skip it
    }
  }
  return items;
}

async function loadCollectedAt() {
  try {
    const data = JSON.parse(await readFile(collectedAtPath, 'utf8'));
    return typeof data.last_collected_at === 'string' ? data.last_collected_at : null;
  } catch {
    return null;
  }
}

function formatChinaTime(iso) {
  const date = new Date(iso);
  if (!iso || Number.isNaN(date.getTime())) {
    return null;
  }
  const shifted = new Date(date.getTime() + 8 * 60 * 60 * 1000);
  const pad = (value) => String(value).padStart(2, '0');
  return `${shifted.getUTCFullYear()}-${pad(shifted.getUTCMonth() + 1)}-${pad(shifted.getUTCDate())} ${pad(shifted.getUTCHours())}:${pad(shifted.getUTCMinutes())}`;
}

function buildHomePage(articles, items, tagCount, collectedAt) {
  const realArticles = articles.filter((article) => article.input_type !== 'demo');
  const sources = buildSourceStats(realArticles, items);
  const latestDate = realArticles.length ? realArticles[0].date : null;
  // `ignored` episodes are not part of the collection readers can process, so exclude them here.
  const collectedItems = items.filter((item) => item.status !== 'ignored');
  const totalSeconds = collectedItems.reduce(
    (sum, item) => sum + (typeof item.duration_seconds === 'number' ? item.duration_seconds : 0),
    0
  );
  const hours = Math.round(totalSeconds / 3600);
  const collectedAtText = formatChinaTime(collectedAt);
  const lines = [
    '---',
    'layout: home',
    'pageClass: home-page',
    'title: EchoForge',
    'hero:',
    '  name: EchoForge',
    '  text: 读懂值得听的技术播客',
    '  tagline: 中文精编、关键观点与原文定位，帮助你快速判断哪些内容值得深入阅读或回听。',
    '  image:',
    '    src: /logo.svg',
    '    alt: EchoForge',
    '  actions:',
    '    - text: 浏览文章',
    '      link: /recent/',
    '      theme: brand',
    '    - text: 浏览节目',
    '      link: /podcasts/',
    '      theme: alt',
    '---',
    '',
    '## 运行统计',
    '',
    `- 已收录 ${sources.length} 档节目，共 ${collectedItems.length} 期，约 ${hours} 小时音频`,
    `- 已发布 ${realArticles.length} 篇文章，提炼 ${tagCount} 个主题标签`,
    `- 最近收录时间：${collectedAtText ?? '暂无'}`,
    `- 最近整理时间：${latestDate ?? '暂无'}`,
    ''
  ];
  return lines.join('\n');
}

function buildSourceStats(articles, items) {
  const sources = new Map();
  for (const item of items) {
    // `ignored` episodes are deliberately excluded from what readers can process.
    if (item.status === 'ignored') {
      continue;
    }
    const id = item.source_id;
    if (!sources.has(id)) {
      sources.set(id, { id, name: item.source_name ?? id, itemCount: 0, articleCount: 0, latest: null });
    }
    const source = sources.get(id);
    source.itemCount += 1;
    source.name = item.source_name ?? source.name;
  }
  for (const article of articles) {
    const [sourceId] = article.path.split('/');
    const source = sources.get(sourceId) ?? {
      id: sourceId,
      name: article.source_name ?? sourceId,
      itemCount: 0,
      articleCount: 0,
      latest: null
    };
    if (!sources.has(sourceId)) {
      sources.set(sourceId, source);
    }
    source.articleCount += 1;
    if (!source.latest || article.date > source.latest) {
      source.latest = article.date;
    }
  }
  return [...sources.values()].sort(
    (left, right) => right.articleCount - left.articleCount || left.name.localeCompare(right.name, 'en')
  );
}

async function listArticlePaths() {
  const entries = await readdir(postsDirectory, { withFileTypes: true, recursive: true });
  return entries
    .filter((entry) => entry.isFile() && entry.name.endsWith('.md') && entry.name !== 'index.md')
    .map((entry) => relative(postsDirectory, join(entry.parentPath, entry.name)).split('\\').join('/'))
    .sort((left, right) => left.localeCompare(right, 'en'));
}

async function removeStaleGeneratedFiles() {
  // Show pages used to be generated as site/posts/<source_id>/index.md; they now live under
  // site/podcasts/. Remove leftovers so local rebuilds never serve both locations.
  const entries = await readdir(postsDirectory, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.isDirectory()) {
      await rm(join(postsDirectory, entry.name, 'index.md'), { force: true });
    }
  }
  await rm(podcastsDirectory, { recursive: true, force: true });
}

async function buildIndex() {
  await removeStaleGeneratedFiles();
  const articlePaths = await listArticlePaths();
  const items = await loadItems();

  const articles = await Promise.all(
    articlePaths.map(async (articlePath) => {
      const path = join(postsDirectory, articlePath);
      const source = await readFile(path, 'utf8');
      const frontmatter = parseFrontmatter(source, path);
      const slug = articlePath.replace(/\.md$/, '');

      return {
        ...frontmatter,
        tags: parseTags(frontmatter.tags),
        reading_minutes: (source.match(/全文共 \d+ 字 · 阅读约 (\d+) 分钟/) ?? [])[1] ?? '1',
        path: articlePath,
        slug
      };
    })
  );

  articles.sort((left, right) => {
    const dateOrder = right.date.localeCompare(left.date);
    if (dateOrder !== 0) {
      return dateOrder;
    }

    const titleOrder = left.title.localeCompare(right.title, 'zh-CN');
    if (titleOrder !== 0) {
      return titleOrder;
    }

    return left.item_id.localeCompare(right.item_id, 'en');
  });

  await writeFile(indexPath, buildAllArticlesPage(articles), 'utf8');
  console.log(`Generated ${relative(projectRoot, indexPath)}.`);

  await mkdir(recentDirectory, { recursive: true });
  await writeFile(recentPath, buildRecentPage(articles), 'utf8');
  console.log(`Generated ${relative(projectRoot, recentPath)}.`);

  const tagMap = new Map();
  for (const article of articles.filter((candidate) => candidate.input_type !== 'demo')) {
    for (const tag of article.tags) {
      if (!tagMap.has(tag)) {
        tagMap.set(tag, []);
      }
      tagMap.get(tag).push(article);
    }
  }

  const tagEntries = [...tagMap.entries()].sort(
    ([leftTag, leftArticles], [rightTag, rightArticles]) =>
      rightArticles.length - leftArticles.length || leftTag.localeCompare(rightTag, 'zh-CN')
  );

  const tagCloud = tagEntries.length
    ? `<div class="tag-cloud">\n${tagEntries
        .map(
          ([tag, taggedArticles]) =>
            `<a class="tag-pill" href="./${tagHref(tag)}"><span class="tag-name">${escapeHtml(tag)}</span><span class="tag-count">${taggedArticles.length} 篇</span></a>`
        )
        .join('\n')}\n</div>`
    : '> 还没有带标签的文章。';
  const tagsOutput = `---\nlayout: doc
pageClass: article-list\ntitle: 标签\nprev: false\nnext: false\n---\n\n# 标签\n\n按标签浏览 EchoForge 已发布的中文技术播客笔记：胶囊按文章数排序，右侧是标签下的文章数。单篇文章通常保留 2～4 个标签。\n\n${tagCloud}\n`;

  await mkdir(tagsDirectory, { recursive: true });
  await writeFile(tagsPath, tagsOutput, 'utf8');

  for (const [tag, taggedArticles] of tagEntries) {
    const page = `---\nlayout: doc
pageClass: article-list\ntitle: ${yamlQuote(tag)}\nprev: false\nnext: false\n---\n\n# ${escapeMarkdown(tag)}\n\n标签「${escapeMarkdown(tag)}」下的中文技术播客笔记，按整理日期倒序。\n\n${taggedArticles.map((article) => articleLink(article, '../../posts/')).join('\n')}\n`;
    const tagDirectory = join(tagsDirectory, tag);
    await mkdir(tagDirectory, { recursive: true });
    await writeFile(join(tagDirectory, 'index.md'), page, 'utf8');
  }
  console.log(`Generated ${relative(projectRoot, tagsPath)} and ${tagEntries.length} tag page(s).`);

  const collectedAt = await loadCollectedAt();
  await writeFile(homePath, `${buildHomePage(articles, items, tagMap.size, collectedAt)}\n`, 'utf8');
  console.log(`Generated ${relative(projectRoot, homePath)}.`);

  const sources = buildSourceStats(
    articles.filter((article) => article.input_type !== 'demo'),
    items
  );

  const podcastSections = sources.length
    ? sources
        .map((source) => {
          const sourceLink = source.articleCount ? `/podcasts/${source.id}/` : null;
          const heading = sourceLink
            ? `### [${escapeMarkdown(source.name)}](${sourceLink})`
            : `### ${escapeMarkdown(source.name)}`;
          return [
            heading,
            '',
            escapeMarkdown(sourceDescriptions[source.id] ?? `${source.name} 的中文技术播客内容。`),
            '',
            `已整理 ${source.articleCount} 期 · 收录 ${source.itemCount} 期`,
            ''
          ].join('\n');
        })
        .join('\n')
    : '> 还没有收录节目。';
  const podcastsPage = `---\nlayout: doc
pageClass: article-list\ntitle: 节目\nprev: false\nnext: false\n---\n\n# 节目\n\nEchoForge 收录的技术播客。「已整理」是已发布中文精编的期数，「收录」是进入处理流程的期数；点开节目名可浏览各期笔记。\n\n${podcastSections}\n`;
  await mkdir(podcastsDirectory, { recursive: true });
  await writeFile(podcastsIndexPath, podcastsPage, 'utf8');
  console.log(`Generated ${relative(projectRoot, podcastsIndexPath)}.`);

  for (const source of sources.filter((candidate) => candidate.articleCount > 0)) {
    const sourceArticles = articles.filter((article) => article.path.startsWith(`${source.id}/`));
    const sections = sourceArticles.length
      ? sourceArticles
          .map(
            (article) =>
              `- [${escapeMarkdown(article.title)}](/posts/${article.path})\n  - ${escapeMarkdown(article.summary)}\n  - 整理日期：${article.date} · 阅读约 ${readingMinutes(article)} 分钟`
          )
          .join('\n')
      : '> 暂无已发布文章。';
    const page = `---\nlayout: doc
pageClass: article-list\ntitle: ${yamlQuote(source.name)}\nprev: false\nnext: false\n---\n\n# ${escapeMarkdown(source.name)}\n\n${escapeMarkdown(sourceDescriptions[source.id] ?? `${source.name} 的中文技术播客内容。`)}\n\n已整理 ${source.articleCount} 期 · 收录 ${source.itemCount} 期\n\n## 已整理内容\n\n${sections}\n`;
    const sourceDirectory = join(podcastsDirectory, source.id);
    await mkdir(sourceDirectory, { recursive: true });
    await writeFile(join(sourceDirectory, 'index.md'), page, 'utf8');
  }
  console.log(`Generated ${sources.filter((source) => source.articleCount > 0).length} show page(s).`);

  const years = [
    ...new Set(articles.filter((article) => article.input_type !== 'demo').map((article) => article.date.slice(0, 4)))
  ].sort((left, right) => right.localeCompare(left));
  const sidebar = [
    {
      text: '导航',
      items: [
        { text: '最近整理', link: '/recent/' },
        {
          text: '全部文章',
          link: '/posts/',
          collapsed: false,
          // VitePress slugifies digit-leading headings like 「## 2026」 to _2026.
          items: years.map((year) => ({ text: year, link: `/posts/#_${year}` }))
        },
        { text: '标签', link: '/tags/' }
      ]
    }
  ];
  if (sources.some((source) => source.articleCount > 0)) {
    sidebar.push({
      text: '节目',
      items: sources
        .filter((source) => source.articleCount > 0)
        .map((source) => ({ text: source.name, link: `/podcasts/${source.id}/` }))
    });
  }
  await mkdir(dirname(sidebarDataPath), { recursive: true });
  await writeFile(sidebarDataPath, `${JSON.stringify(sidebar, null, 2)}\n`, 'utf8');
  console.log(`Generated ${relative(projectRoot, sidebarDataPath)}.`);

  // Chronology for the article pager: newest first, the same order as the 全部文章 page.
  // `text` is the key VitePress frontmatter prev/next expects.
  const postsOrder = articles
    .filter((article) => article.input_type !== 'demo')
    .map((article) => ({ text: article.title, link: `/posts/${article.slug}` }));
  await mkdir(dirname(postsOrderPath), { recursive: true });
  await writeFile(postsOrderPath, `${JSON.stringify(postsOrder, null, 2)}\n`, 'utf8');
  console.log(`Generated ${relative(projectRoot, postsOrderPath)}.`);
}

buildIndex().catch((error) => {
  console.error(`Failed to generate article index: ${error.message}`);
  process.exitCode = 1;
});
