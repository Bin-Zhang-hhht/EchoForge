import { mkdir, readdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const requiredFields = ['item_id', 'title', 'date', 'source_url'];
const scriptDirectory = fileURLToPath(new URL('.', import.meta.url));
const projectRoot = join(scriptDirectory, '..');
const postsDirectory = join(projectRoot, 'site', 'posts');
const indexPath = join(postsDirectory, 'index.md');
const tagsDirectory = join(projectRoot, 'site', 'tags');
const tagsPath = join(tagsDirectory, 'index.md');
const sidebarDataPath = join(projectRoot, 'site', '.vitepress', 'sidebar.data.json');

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
  return `- [${escapeMarkdown(article.title)}](${linkPrefix}${article.path})\n  - 整理日期：${article.date}\n  - 来源：[${escapeMarkdown(article.source_name ?? article.source_url)}](${article.source_url})`;
}

async function listArticlePaths() {
  const entries = await readdir(postsDirectory, { withFileTypes: true, recursive: true });
  return entries
    .filter((entry) => entry.isFile() && entry.name.endsWith('.md') && entry.name !== 'index.md')
    .map((entry) => relative(postsDirectory, join(entry.parentPath, entry.name)).split('\\').join('/'))
    .sort((left, right) => left.localeCompare(right, 'en'));
}

async function buildIndex() {
  const articlePaths = await listArticlePaths();

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

  const list = articles.length
    ? articles.map((article) => articleLink(article, './')).join('\n')
    : '> 还没有可发布的文章。\n';

  const output = `---\nlayout: doc\ntitle: 文章\n---\n\n# 文章\n\n这里列出 EchoForge 已发布的中文技术播客笔记。文章按整理日期倒序排列。\n\n${list}\n`;

  await mkdir(postsDirectory, { recursive: true });
  await writeFile(indexPath, output, 'utf8');
  console.log(`Generated ${relative(projectRoot, indexPath)} from ${articles.length} article(s).`);

  const tagMap = new Map();
  for (const article of articles) {
    for (const tag of article.tags) {
      if (!tagMap.has(tag)) {
        tagMap.set(tag, []);
      }
      tagMap.get(tag).push(article);
    }
  }

  const tagSections = [...tagMap.entries()]
    .sort(([left], [right]) => left.localeCompare(right, 'zh-CN'))
    .map(([tag, taggedArticles]) => `## ${escapeMarkdown(tag)}\n\n${taggedArticles.map((article) => articleLink(article, '../posts/')).join('\n')}`)
    .join('\n\n');

  const tagsOutput = `---\nlayout: doc\ntitle: 标签\n---\n\n# 标签\n\n按标签浏览 EchoForge 已发布的中文技术播客笔记。\n\n${tagSections || '> 还没有带标签的文章。\n'}\n`;

  await mkdir(tagsDirectory, { recursive: true });
  await writeFile(tagsPath, tagsOutput, 'utf8');
  console.log(`Generated ${relative(projectRoot, tagsPath)} from ${tagMap.size} tag(s).`);

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
        { text: '全部文章', link: '/posts/' },
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
