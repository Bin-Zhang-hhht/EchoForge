import { defineConfig } from 'vitepress';
import sidebar from './sidebar.data.json';
import postsOrder from './posts-order.json';

const orderIndex = new Map(postsOrder.map((article, index) => [article.link, index]));

export default defineConfig({
  lang: 'zh-CN',
  title: 'EchoForge',
  description: '技术播客的中文阅读雷达',
  base: '/EchoForge/',
  cleanUrls: true,
  head: [['link', { rel: 'icon', type: 'image/svg+xml', href: '/EchoForge/logo.svg' }]],
  transformPageData(pageData) {
    const index = orderIndex.get(`/${pageData.relativePath.replace(/\.md$/, '')}`);
    if (index === undefined) {
      return;
    }
    // 上一篇 is the newer digest, 下一篇 the older one, matching the 全部文章 order.
    // Edges are explicit false so the theme never falls back to sidebar-derived links.
    pageData.frontmatter.prev = index > 0 ? postsOrder[index - 1] : false;
    pageData.frontmatter.next = index < postsOrder.length - 1 ? postsOrder[index + 1] : false;
  },
  themeConfig: {
    logo: '/logo.svg',
    nav: [
      { text: '文章', link: '/recent/' },
      { text: '节目', link: '/podcasts/' },
      { text: '标签', link: '/tags/' }
    ],
    sidebar: {
      '/posts/': sidebar,
      '/tags/': sidebar,
      '/podcasts/': sidebar,
      '/recent/': sidebar
    },
    socialLinks: [{ icon: 'github', link: 'https://github.com/Bin-Zhang-hhht/EchoForge' }],
    search: {
      provider: 'local'
    },
    footer: {
      message: 'AI 编辑整理，请以原始节目为准。',
      copyright: 'EchoForge'
    },
    docFooter: {
      prev: '上一篇',
      next: '下一篇'
    }
  }
});
