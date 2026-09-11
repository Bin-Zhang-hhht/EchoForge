import { defineConfig } from 'vitepress';
import sidebar from './sidebar.data.json';

export default defineConfig({
  lang: 'zh-CN',
  title: 'EchoForge',
  description: '技术播客的中文阅读雷达',
  base: '/EchoForge/',
  cleanUrls: true,
  head: [['link', { rel: 'icon', type: 'image/svg+xml', href: '/EchoForge/logo.svg' }]],
  themeConfig: {
    logo: '/logo.svg',
    nav: [
      { text: '首页', link: '/' },
      { text: '文章', link: '/posts/' },
      { text: '标签', link: '/tags/' }
    ],
    sidebar: {
      '/posts/': sidebar,
      '/tags/': sidebar
    },
    socialLinks: [{ icon: 'github', link: 'https://github.com/Bin-Zhang-hhht/EchoForge' }],
    search: {
      provider: 'local'
    },
    footer: {
      message: 'AI 编辑整理，请以原始节目为准。',
      copyright: 'EchoForge'
    }
  }
});
