import os
from ntscraper import Nitter
from feedgen.feed import FeedGenerator

def generate_rss():
    # 准备多个备用实例，防止 403 或抓取失败
    instances = ["https://nitter.privacydev.net", "https://xcancel.com", "https://nitter.net.in"]
    tweets = None
    
    for instance in instances:
        try:
            print(f"正在尝试从 {instance} 抓取 #heartheartart...")
            scraper = Nitter(instance=instance)
            tweets = scraper.get_tweets("heartheartart", mode="hashtag", number=10)
            if tweets and tweets['tweets']:
                print(f"抓取成功！获取到 {len(tweets['tweets'])} 条推文")
                break
        except Exception as e:
            print(f"实例 {instance} 失败: {e}")
            continue

    if not tweets or not tweets['tweets']:
        print("所有实例均抓取失败，跳过本次生成。")
        return

    # 创建 RSS
    fg = FeedGenerator()
    fg.title('Evil Neuro Fanart Feed')
    fg.link(href='https://twitter.com/hashtag/heartheartart')
    fg.description('Automatic RSS for #heartheartart')

    for tweet in tweets['tweets']:
        fe = fg.add_entry()
        fe.title(tweet['text'][:50] if tweet['text'] else "New Art")
        fe.link(href=tweet['link'])
        
        # 组装带图片的描述
        desc = tweet['text'] + "<br>"
        for img in tweet['pictures']:
            desc += f'<img src="{img}"><br>'
        fe.description(desc)
        fe.pubDate(tweet['date'])

    # 显式保存文件
    fg.rss_file('feed.xml')
    print("feed.xml 已成功保存到当前目录")

if __name__ == "__main__":
    generate_rss()
