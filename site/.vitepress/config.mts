import { defineConfig } from 'vitepress';

export default defineConfig({
  lang: 'zh-CN',
  title: 'EchoForge',
  description: '技术播客的中文阅读雷达',
  base: '/EchoForge/',
  cleanUrls: true,
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '文章', link: '/posts/' },
      { text: '项目文档', link: 'https://github.com/Bin-Zhang-hhht/EchoForge' }
    ],
    sidebar: {
      '/posts/': [
        {
          text: '文章',
          items: [{ text: '全部文章', link: '/posts/' }]
        }
      ]
    },
    search: {
      provider: 'local'
    },
    footer: {
      message: 'AI 编辑整理，请以原始节目为准。',
      copyright: 'EchoForge'
    }
  }
});
