import os
from ntscraper import Nitter
from feedgen.feed import FeedGenerator
from datetime import datetime

def generate_rss():
    # 1. 初始化抓取器
    scraper = Nitter()
    
    # 尝试在不同的 Nitter 实例中抓取，防止单个实例 403
    # 抓取话题 #heartheartart
    try:
        print("正在抓取推文...")
        tweets = scraper.get_tweets("heartheartart", mode="hashtag", number=15)
    except Exception as e:
        print(f"抓取失败: {e}")
        return

    # 2. 创建 RSS 生成器
    fg = FeedGenerator()
    fg.title('Evil Neuro Fanart Feed')
    fg.link(href='https://twitter.com/hashtag/heartheartart')
    fg.description('自动追踪 #heartheartart 话题的最新推文')
    fg.language('zh-CN')

    # 3. 填充内容
    for tweet in tweets['tweets']:
        fe = fg.add_entry()
        fe.title(tweet['text'][:50] if tweet['text'] else "新二创图片推送")
        fe.link(href=tweet['link'])
        
        # 组装描述内容（包含正文和图片）
        content = tweet['text'] + "<br><br>"
        for img in tweet['pictures']:
            content += f'<img src="{img}"><br>'
        
        fe.description(content)
        fe.pubDate(tweet['date'])

    # 4. 保存为文件
    fg.rss_file('feed.xml')
    print("RSS 文件已生成")

if __name__ == "__main__":
    generate_rss()
