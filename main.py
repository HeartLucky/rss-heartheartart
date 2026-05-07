import os
import sys
from ntscraper import Nitter
from feedgen.feed import FeedGenerator

def generate_rss():
    # 增加更多备用地址，并打印调试信息
    instances = [
        "https://nitter.privacydev.net", 
        "https://xcancel.com", 
        "https://nitter.net.in",
        "https://nitter.moomoo.me"
    ]
    tweets = None
    
    print("开始抓取流程...")
    
    for instance in instances:
        try:
            print(f"尝试实例: {instance}")
            scraper = Nitter(instance=instance)
            # 抓取话题 #heartheartart
            tweets = scraper.get_tweets("heartheartart", mode="hashtag", number=10)
            
            if tweets and 'tweets' in tweets and len(tweets['tweets']) > 0:
                print(f"成功！从 {instance} 抓取到 {len(tweets['tweets'])} 条推文。")
                break
            else:
                print(f"警告：实例 {instance} 返回了空列表。")
        except Exception as e:
            print(f"实例 {instance} 报错: {str(e)}")
            continue

    if not tweets or not tweets.get('tweets'):
        print("错误：所有实例都无法获取数据。可能是 X 的反爬加强了。")
        # 即使没抓到，我们也生成一个空的 RSS 文件，防止 Workflow 报错 128
        create_empty_feed()
        return

    try:
        fg = FeedGenerator()
        fg.title('Evil Neuro Fanart Feed')
        fg.link(href='https://twitter.com/hashtag/heartheartart')
        fg.description('Automatic RSS for #heartheartart')

        for tweet in tweets['tweets']:
            fe = fg.add_entry()
            fe.title(tweet['text'][:50] if tweet['text'] else "New Art")
            fe.link(href=tweet['link'])
            
            desc = tweet['text'] + "<br>"
            if 'pictures' in tweet:
                for img in tweet['pictures']:
                    desc += f'<img src="{img}"><br>'
            fe.description(desc)
            fe.pubDate(tweet['date'])

        # 确保文件被写入
        output_path = 'feed.xml'
        fg.rss_file(output_path)
        print(f"文件已成功保存至: {os.path.abspath(output_path)}")
        
    except Exception as e:
        print(f"生成 RSS 文件时发生错误: {e}")

def create_empty_feed():
    """创建一个基础的 RSS 文件防止报错"""
    fg = FeedGenerator()
    fg.title('Empty Feed')
    fg.link(href='https://github.com')
    fg.description('No data fetched yet')
    fg.rss_file('feed.xml')
    print("已创建占位用的空 feed.xml")

if __name__ == "__main__":
    generate_rss()
