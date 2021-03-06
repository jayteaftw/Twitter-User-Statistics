

import asyncio
from pyppeteer import launch


async def main():
    
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto('https://twitter.com/elonmusk')
    await asyncio.sleep(5)

    pages = 10
    for i in range(pages):
        await page.evaluate('() => window.scrollTo(0,document.body.scrollHeight)')
        await asyncio.sleep(1)

    tweets = []

    tweet_elements = await page.xpath('//ol[@id="stream-items-id"]//div[@class="content"]')
    
    for elem in tweet_elements:
        # Select the element handles we need
        title = await elem.xpath('.//strong[contains(@class, "fullname")]')
        comments = await elem.xpath('.//button[contains(@class, "js-actionReply")]//span[@class="ProfileTweet-actionCountForPresentation"]')
        retweets = await elem.xpath('.//button[contains(@class, "js-actionRetweet")]//span[@class="ProfileTweet-actionCountForPresentation"]')
        likes = await elem.xpath('.//button[contains(@class, "js-actionFavorite")]//span[@class="ProfileTweet-actionCountForPresentation"]')
        
        # Decode each handle, getting its text value
        name_value = await page.evaluate('(elem) => elem.innerHTML',title[0])
        comment_count = await page.evaluate('(elem) => elem.innerHTML',comments[0])
        retweet_count = await page.evaluate('(elem) => elem.innerHTML',retweets[0])
        like_count = await page.evaluate('(elem) => elem.innerHTML',likes[0])

        # Commit the data we got from this tweet to our list. We use a tuple here because of convension.
        tweets.append((name_value, comment_count, retweet_count, like_count))


    print(tweets)

    await browser.close()




asyncio.get_event_loop().run_until_complete(main())

