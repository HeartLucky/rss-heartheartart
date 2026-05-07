import os
import random
import time
from ntscraper import Nitter
from feedgen.feed import FeedGenerator

def generate_rss():
    # 从健康监测站筛选出的 RSS 支持良好且健康的实例
    instances = [
        "https://nitter.net",
        "https://xcancel.com",
        "https://nitter.poast.org",
        "https://nitter.privacyredirect.com",
        "https://nitter.perennialte.ch",
        "https://nitter.esmailelbob.xyz",
        "https://nitter.projectsegfau.lt"
    ]
    
    # 随机打乱顺序，每次运行选不同的实例开始尝试，防止死磕一个 IP
    random.shuffle(instances)
    
    tweets = None
    target_hashtag = "heartheartart"
    
    print(f"--- 开始二创追踪任务：#{target_hashtag} ---")
    
    for instance in instances:
        try:
            print(f"正在尝试连接实例: {instance}")
            # 加入随机小延迟，模拟人类行为
            time.sleep(random.uniform(1, 3))
            
            scraper = Nitter(instance=instance)
            tweets = scraper.get_tweets(target_hashtag, mode="hashtag", number=10)
            
            if tweets and 'tweets' in tweets and len(tweets['tweets']) > 0:
                print(f"成功！从 {instance} 抓取到 {len(tweets['tweets'])} 条最新动态。")
                break
            else:
                print(f"警告：实例 {instance} 未返回推文（可能被限流或无更新）。")
        except Exception as e:
            print(f"跳过故障实例 {instance}，错误信息: {e}")
            continue

    # 如果所有实例都失败，生成一个占位文件防止 Workflow 报错
    if not tweets or not tweets.get('tweets'):
        print("!!! 关键错误：本次所有实例均未获取到数据。")
        create_empty_feed()
        return

    # --- 开始构建 RSS 文件 ---
    try:
        fg = FeedGenerator()
        fg.title(f'#{target_hashtag} Art Feed')
        fg.link(href=f'https://twitter.com/hashtag/{target_hashtag}')
        fg.description(f'Evil Neuro 二创话题 #{target_hashtag} 的自动追踪站')
        fg.language('zh-CN')

        for tweet in tweets['tweets']:
            fe = fg.add_entry()
            fe.title(tweet['text'][:50].replace('\n', ' ') if tweet['text'] else "New Art Post")
            fe.link(href=tweet['link'])
            
            # 这里的描述逻辑：文字 + 图片
            content = f"内容: {tweet['text']}<br><br>"
            if 'pictures' in tweet:
                for img in tweet['pictures']:
                    # 提示：如果以后要原图，可以在这里处理 img 字符串
                    content += f'<img src="{img}" style="max-width:100%;"><br>'
            
            fe.description(content)
            fe.pubDate(tweet['date'])

        fg.rss_file('feed.xml')
        print(f"✅ RSS 任务完成！feed.xml 已更新。")
        
    except Exception as e:
        print(f"构建 RSS 逻辑发生错误: {e}")

def create_empty_feed():
    fg = FeedGenerator()
    fg.title('Evil Neuro Art Tracker (Waiting)')
    fg.link(href='https://github.com')
    fg.description('目前没有抓取到新推文，正在等待下一轮自动运行。')
    fg.rss_file('feed.xml')
    print("已生成占位 Feed 确保 Workflow 绿色运行。")

if __name__ == "__main__":
    generate_rss()
