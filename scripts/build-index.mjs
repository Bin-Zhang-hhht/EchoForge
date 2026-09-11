import { mkdir, readdir, readFile, writeFile } from 'node:fs/promises';
import { basename, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const requiredFields = ['item_id', 'title', 'date', 'source_url'];
const scriptDirectory = fileURLToPath(new URL('.', import.meta.url));
const projectRoot = join(scriptDirectory, '..');
const postsDirectory = join(projectRoot, 'site', 'posts');
const indexPath = join(postsDirectory, 'index.md');

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

function escapeMarkdown(text) {
  return text.replace(/([\\[\]])/g, '\\$1');
}

async function buildIndex() {
  const entries = await readdir(postsDirectory, { withFileTypes: true });
  const articleFiles = entries
    .filter((entry) => entry.isFile() && entry.name.endsWith('.md') && entry.name !== 'index.md')
    .map((entry) => entry.name)
    .sort((left, right) => left.localeCompare(right, 'en'));

  const articles = await Promise.all(
    articleFiles.map(async (filename) => {
      const path = join(postsDirectory, filename);
      const source = await readFile(path, 'utf8');
      const frontmatter = parseFrontmatter(source, path);

      return {
        ...frontmatter,
        filename,
        slug: basename(filename, '.md')
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
    ? articles
        .map((article) => `- [${escapeMarkdown(article.title)}](./${article.slug}.md)\n  - 整理日期：${article.date}\n  - 来源：[${escapeMarkdown(article.source_name ?? article.source_url)}](${article.source_url})`)
        .join('\n')
    : '> 还没有可发布的文章。\n';

  const output = `---\nlayout: doc\ntitle: 文章\n---\n\n# 文章\n\n这里列出 EchoForge 已发布的中文技术播客笔记。文章按整理日期倒序排列。\n\n${list}\n`;

  await mkdir(postsDirectory, { recursive: true });
  await writeFile(indexPath, output, 'utf8');
  console.log(`Generated ${relative(projectRoot, indexPath)} from ${articles.length} article(s).`);
}

buildIndex().catch((error) => {
  console.error(`Failed to generate article index: ${error.message}`);
  process.exitCode = 1;
});
