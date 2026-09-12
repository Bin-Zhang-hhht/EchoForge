import { mkdir, readdir, readFile, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { dirname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const requiredFields = ['item_id', 'title', 'date', 'source_url'];
const scriptDirectory = fileURLToPath(new URL('.', import.meta.url));
const projectRoot = join(scriptDirectory, '..');
const postsDirectory = join(projectRoot, 'site', 'posts');
const indexPath = join(postsDirectory, 'index.md');
const tagsDirectory = join(projectRoot, 'site', 'tags');
const tagsPath = join(tagsDirectory, 'index.md');
const homePath = join(projectRoot, 'site', 'index.md');
const sidebarDataPath = join(projectRoot, 'site', '.vitepress', 'sidebar.data.json');
const dataDirectory = join(projectRoot, 'data', 'items');
const publicDirectory = join(projectRoot, 'site', 'public');
const siteBase = '/EchoForge/'; // keep in sync with site/.vitepress/config.mts base

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

function yamlQuote(value) {
  return `'${String(value).replace(/'/g, "''")}'`;
}

function groupBySource(articles) {
  const sources = new Map();
  for (const article of articles) {
    const parts = article.path.split('/');
    if (parts.length !== 3) {
      continue;
    }
    const [sourceId, year] = parts;
    if (!sources.has(sourceId)) {
      sources.set(sourceId, { id: sourceId, name: article.source_name ?? sourceId, articles: [] });
    }
    sources.get(sourceId).articles.push({ ...article, year, href: `./${parts.slice(1).join('/')}` });
  }
  return [...sources.values()].sort(
    (left, right) =>
      right.articles.length - left.articles.length || left.name.localeCompare(right.name, 'en')
  );
}

function articleLink(article, linkPrefix) {
  const lines = [
    `- [${escapeMarkdown(article.title)}](${linkPrefix}${article.path})`,
    `  - 整理日期：${article.date}`
  ];
  if (article.published_at) {
    lines.push(`  - 节目发布：${article.published_at}`);
  }
  lines.push(`  - 来源：[${escapeMarkdown(article.source_name ?? article.source_url)}](${article.source_url})`);
  return lines.join('\n');
}

function localDateString(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function buildWeeklyPage(articles) {
  const today = localDateString(new Date());
  const cutoff = localDateString(new Date(Date.now() - 7 * 24 * 60 * 60 * 1000));
  const weeklyArticles = articles.filter(
    (article) => article.input_type !== 'demo' && article.date >= cutoff && article.date <= today
  );

  const lines = [
    '---',
    'layout: doc',
    'title: 本周速览',
    '---',
    '',
    '# 本周速览',
    '',
    `最近 7 天整理的中文技术播客精编（截至 ${today}）。要看更早的内容请前往[全部文章](./all/)。`,
    ''
  ];
  if (weeklyArticles.length) {
    lines.push(...weeklyArticles.map((article) => articleLink(article, './')), '');
  } else {
    lines.push(`> 最近 7 天没有新整理的精编。已有内容见[全部文章](./all/)。`, '');
  }
  return lines.join('\n');
}

function buildAllArticlesPage(articles) {
  const byYear = new Map();
  for (const article of articles) {
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
        `## ${year}\n\n${byYear.get(year).map((article) => articleLink(article, '../')).join('\n')}`
    )
    .join('\n\n');

  const body = sections || '> 还没有可发布的文章。';
  return `---\nlayout: doc\ntitle: 全部文章\n---\n\n# 全部文章\n\nEchoForge 已发布的全部中文技术播客笔记，按整理年份分组，年份内按整理日期倒序。\n\n${body}\n`;
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

function buildSourceStats(articles, items) {
  const sources = new Map();
  for (const item of items) {
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
    const source = sources.get(sourceId);
    if (!source) {
      continue;
    }
    source.articleCount += 1;
    if (!source.latest || article.date > source.latest) {
      source.latest = article.date;
    }
  }
  return [...sources.values()].sort(
    (left, right) =>
      right.articleCount - left.articleCount || left.name.localeCompare(right.name, 'en')
  );
}

async function buildHomePage(articles, items, tagCount) {
  const realArticles = articles.filter((article) => article.path.split('/').length === 3);
  const sources = buildSourceStats(realArticles, items);
  const pending = items.filter((item) => item.status === 'pending').length;
  const totalSeconds = items.reduce(
    (sum, item) => sum + (typeof item.duration_seconds === 'number' ? item.duration_seconds : 0),
    0
  );
  const hours = Math.round(totalSeconds / 3600);
  const covered = sources.filter((source) => source.articleCount > 0).length;
  const latestDate = realArticles.length ? realArticles[0].date : null;

  const features = [
    {
      icon: '📝',
      title: `${realArticles.length} 篇精编`,
      details: latestDate ? `最近整理 ${latestDate}` : '精编即将发布',
      link: '/posts/',
      linkText: '浏览文章'
    },
    {
      icon: '⏳',
      title: `${pending} 条待处理`,
      details: `已收录 ${items.length} 期节目素材`
    },
    {
      icon: '🎙️',
      title: `${covered} 档节目已精编`,
      details: `共收录 ${sources.length} 档 · 约 ${hours} 小时音频`
    },
    {
      icon: '🏷️',
      title: `${tagCount} 个主题标签`,
      details: '按主题浏览同类内容',
      link: '/tags/',
      linkText: '查看标签'
    }
  ];
  for (const source of sources) {
    features.push(
      source.articleCount
        ? {
            icon: '📻',
            title: source.name,
            details: `精编 ${source.articleCount} 篇 · 收录 ${source.itemCount} 期 · 最近整理 ${source.latest}`,
            link: `/posts/${source.id}/`,
            linkText: '进入节目'
          }
        : {
            icon: '📻',
            title: source.name,
            details: `收录 ${source.itemCount} 期素材，精编整理中`
          }
    );
  }

  const hero = {
    name: 'EchoForge',
    text: '技术播客中文阅读雷达',
    tagline: '从公开技术访谈保存完整逐字稿，生成可追溯的中文精编——先看重点观点与边界，再决定是否回听。',
    actions: [
      { theme: 'brand', text: '浏览文章', link: '/posts/' },
      { theme: 'alt', text: '按标签浏览', link: '/tags/' }
    ]
  };
  for (const extension of ['png', 'jpg', 'jpeg', 'webp', 'avif', 'svg']) {
    const banner = `banner.${extension}`;
    if (existsSync(join(publicDirectory, banner))) {
      hero.image = { src: `${siteBase}${banner}`, alt: 'EchoForge' };
      break;
    }
  }

  const lines = [
    '---',
    'layout: home',
    'hero:',
    `  name: ${yamlQuote(hero.name)}`,
    `  text: ${yamlQuote(hero.text)}`,
    `  tagline: ${yamlQuote(hero.tagline)}`,
    '  actions:'
  ];
  for (const action of hero.actions) {
    lines.push(`    - theme: ${action.theme}`, `      text: ${yamlQuote(action.text)}`, `      link: ${action.link}`);
  }
  if (hero.image) {
    lines.push('  image:', `    src: ${hero.image.src}`, `    alt: ${yamlQuote(hero.image.alt)}`);
  }
  lines.push('features:');
  for (const feature of features) {
    lines.push(
      `  - icon: ${yamlQuote(feature.icon)}`,
      `    title: ${yamlQuote(feature.title)}`,
      `    details: ${yamlQuote(feature.details)}`
    );
    if (feature.link) {
      lines.push(`    link: ${feature.link}`, `    linkText: ${yamlQuote(feature.linkText)}`);
    }
  }
  lines.push('---', '');

  await writeFile(homePath, `${lines.join('\n')}\n`, 'utf8');
  console.log(`Generated ${relative(projectRoot, homePath)} with ${features.length} feature card(s).`);
}

async function listArticlePaths() {
  const entries = await readdir(postsDirectory, { withFileTypes: true, recursive: true });
  return entries
    .filter((entry) => entry.isFile() && entry.name.endsWith('.md') && entry.name !== 'index.md')
    .map((entry) => relative(postsDirectory, join(entry.parentPath, entry.name)).split('\\').join('/'))
    .sort((left, right) => left.localeCompare(right, 'en'));
}

function tagHref(tag) {
  return `${encodeURIComponent(tag).replace(/%2F/gi, '')}/`;
}

async function buildIndex() {
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

  const weeklyPage = buildWeeklyPage(articles);
  await writeFile(indexPath, weeklyPage, 'utf8');
  console.log(`Generated ${relative(projectRoot, indexPath)}.`);

  const allPage = buildAllArticlesPage(articles);
  const allDirectory = join(postsDirectory, 'all');
  await mkdir(allDirectory, { recursive: true });
  await writeFile(join(allDirectory, 'index.md'), allPage, 'utf8');
  console.log(`Generated ${relative(projectRoot, join(postsDirectory, 'all', 'index.md'))}.`);

  const tagMap = new Map();
  for (const article of articles) {
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

  const tagList = tagEntries.length
    ? tagEntries.map(([tag, taggedArticles]) => `- [${escapeMarkdown(tag)}](./${tagHref(tag)}) · ${taggedArticles.length} 篇`).join('\n')
    : '> 还没有带标签的文章。\n';
  const tagsOutput = `---\nlayout: doc\ntitle: 标签\n---\n\n# 标签\n\n按标签浏览 EchoForge 已发布的中文技术播客笔记，标签按文章数排序。\n\n${tagList}\n`;

  await mkdir(tagsDirectory, { recursive: true });
  await writeFile(tagsPath, tagsOutput, 'utf8');

  for (const [tag, taggedArticles] of tagEntries) {
    const page = `---\nlayout: doc\ntitle: ${yamlQuote(tag)}\n---\n\n# ${escapeMarkdown(tag)}\n\n标签「${escapeMarkdown(tag)}」下的中文技术播客笔记，按整理日期倒序。\n\n${taggedArticles.map((article) => articleLink(article, '../../posts/')).join('\n')}\n`;
    const tagDirectory = join(tagsDirectory, tag);
    await mkdir(tagDirectory, { recursive: true });
    await writeFile(join(tagDirectory, 'index.md'), page, 'utf8');
  }
  console.log(`Generated ${relative(projectRoot, tagsPath)} and ${tagEntries.length} tag page(s).`);

  await buildHomePage(articles, items, tagMap.size);

  const sources = groupBySource(articles);
  for (const source of sources) {
    const byYear = new Map();
    for (const article of source.articles) {
      if (!byYear.has(article.year)) {
        byYear.set(article.year, []);
      }
      byYear.get(article.year).push(article);
    }
    const sections = [...byYear.keys()]
      .sort((left, right) => right.localeCompare(left))
      .map(
        (year) =>
          `## ${year}\n\n${byYear.get(year).map((article) => `- [${escapeMarkdown(article.title)}](${article.href})\n  - 整理日期：${article.date}`).join('\n')}`
      )
      .join('\n\n');
    const page = `---\nlayout: doc\ntitle: ${yamlQuote(source.name)}\n---\n\n# ${escapeMarkdown(source.name)}\n\n${escapeMarkdown(source.name)} 节目的中文技术播客笔记，按年份分组、整理日期倒序。\n\n${sections}\n`;
    const sourceDirectory = join(postsDirectory, source.id);
    await mkdir(sourceDirectory, { recursive: true });
    await writeFile(join(sourceDirectory, 'index.md'), page, 'utf8');
  }
  console.log(`Generated ${sources.length} show page(s).`);

  const sidebar = [
    {
      text: '导航',
      items: [
        { text: '本周速览', link: '/posts/' },
        { text: '全部文章', link: '/posts/all/' },
        { text: '标签', link: '/tags/' }
      ]
    }
  ];
  if (sources.length) {
    sidebar.push({
      text: '节目',
      items: sources.map((source) => ({ text: source.name, link: `/posts/${source.id}/` }))
    });
  }
  await mkdir(dirname(sidebarDataPath), { recursive: true });
  await writeFile(sidebarDataPath, `${JSON.stringify(sidebar, null, 2)}\n`, 'utf8');
  console.log(`Generated ${relative(projectRoot, sidebarDataPath)}.`);
}

buildIndex().catch((error) => {
  console.error(`Failed to generate article index: ${error.message}`);
  process.exitCode = 1;
});
