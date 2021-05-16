# 新闻信息收集与分析小组的代码仓库
## 1、安装环境依赖

```python
pip install -r requirements.txt
```
## 2、项目运行

1. 将**latest_url.json**文件初始化为：（初始化json文件在initial.json中）

   ```json
   {
     "Sina": "",
     "NetEase": ""
   }
   ```

2. 运行begin.py文件

   ```python
   from scrapy import cmdline
   cmdline.execute("scrapy crawl spider_filename".split())
   ```

3. latest_url.json用来存储本次爬取的最新新闻url，下次爬取时遇到该url时便自动结束爬虫，实现增量爬取

## 3、项目文件树(结构)及文件说明

```bash
│  .gitignore
│  README.md
│  scrapy.cfg
│
├─Document
└─NewsPro
    │  begin.py
    │  chromedriver.exe
    │  emo_an.py
    │  getsubstr.py
    │  get_muselist.py
    │  get_News_muse.py
    │  initial.json
    │  items.py
    │  middlewares.py
    │  muselist.xlsx
    │  pipelines.py
    │  processed_html.py
    │  requirements.txt
    │  settings.py
    │  time_process.py
    │  __init__.py
    │
    ├─spiders
    │  │  Baidu.py
    │  │  BaijiaHao.py
    │  │  latest_url.json
    │  │  NetEase.py
    │  │  Sina.py
    │  │  __init__.py
    │  │
    │  └─__pycache__
    │          Baidu.cpython-37.pyc
    │          BaijiaHao.cpython-37.pyc
    │          NetEase.cpython-37.pyc
    │          Sina.cpython-37.pyc
    │          __init__.cpython-37.pyc
    │
    └─__pycache__
            emo_an.cpython-37.pyc
            getsubstr.cpython-37.pyc
            get_muselist.cpython-37.pyc
            items.cpython-37.pyc
            middlewares.cpython-37.pyc
            pipelines.cpython-37.pyc
            processed_html.cpython-37.pyc
            settings.cpython-37.pyc
            time_process.cpython-37.pyc
            __init__.cpython-37.pyc
```

1. spider文件夹

   ```
   │  Baidu.py ->百度新闻爬虫，可链接到澎湃新闻、腾讯新闻、搜狐新闻、网易新闻、凤凰新闻等多个平台
   │  BaijiaHao.py ->百度百家号爬虫
   │  latest_url.json ->实现增量爬取的json文件，用来存储上次爬取的最新url
   │  NetEase.py —>网易新闻爬虫，网易新闻的博物馆页面新闻爬取
   │  Sina.py —>新浪新闻爬虫
   │  __init__.py
   │
   └─__pycache__
           Baidu.cpython-37.pyc
           BaijiaHao.cpython-37.pyc
           NetEase.cpython-37.pyc
           Sina.cpython-37.pyc
           __init__.cpython-37.pyc
   ```

   

2. NewsPro文件夹

   ```bash
   │  begin.py ->项目执行文件
   │  chromedriver.exe ->谷歌驱动
   │  emo_an.py —>新闻文本情感分析文件
   │  getsubstr.py ->处理url获取子串文件
   │  get_muselist.py ->获取博物馆列表文件
   │  get_News_muse.py ->获取新闻中出现的博物馆*(由于只有网易爬虫需要调用故写在了NetEase.py中)
   │  initial.json ->json初始化文件
   │  items.py ->scrapy items文件，包括了我们需要存入数据库中的各字段
   │  middlewares.py ->scrapy 中间件文件，包括爬虫中间件、下载中间件(使用selenium处理动态加载)、随机延时爬虫中间件、随机UA生成中间件
   │  muselist.xlsx ->博物馆excel列表
   │  pipelines.py ->管道文件，进行数据库的连接以及数据的存入
   │  processed_html.py ->新闻网页源代码内容的处理文件，使用正则表达式替换标签供前端使用
   │  requirements.txt ->环境依赖包
   │  settings.py ->scrapy 配置文件
   │  time_process.py ->对爬取到的时间信息进行处理
   │  __init__.py
   │
   ├─spiders
   │  │  Baidu.py
   │  │  BaijiaHao.py
   │  │  latest_url.json
   │  │  NetEase.py
   │  │  Sina.py
   │  │  __init__.py
   │  │
   │  └─__pycache__
   │          Baidu.cpython-37.pyc
   │          BaijiaHao.cpython-37.pyc
   │          NetEase.cpython-37.pyc
   │          Sina.cpython-37.pyc
   │          __init__.cpython-37.pyc
   │
   └─__pycache__
           emo_an.cpython-37.pyc
           getsubstr.cpython-37.pyc
           get_muselist.cpython-37.pyc
           items.cpython-37.pyc
           middlewares.cpython-37.pyc
           pipelines.cpython-37.pyc
           processed_html.cpython-37.pyc
           settings.cpython-37.pyc
           time_process.cpython-37.pyc
           __init__.cpython-37.pyc
   ```
