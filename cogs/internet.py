from discord.ext import commands
import discord
import wikipedia
import requests
import re
import random
import urllib


def format_error(error):
    return """```
Error 420 in command
    {}
```""".format(error)


class Internet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["wiki"])
    async def wikipedia(self, ctx, *, search):
        """
        Find a Wikipedia page on a given topic
        """
        await ctx.channel.trigger_typing()
        search = wikipedia.search(search)

        if not search:
            await ctx.send(format_error("No page was found for that search term"))
            return

        page = wikipedia.page(search[0])
        title = page.title
        body = page.summary
        if len(body) >= 2000:
            body = body[:2000].rsplit(" ", 1)[0] + " **-Snippet-**"
        image = page.images[0]
        url = page.url

        embed = discord.Embed(title=title, description=body, url=url)
        embed.set_footer(text="From Wikipedia")
        embed.set_thumbnail(url=image)

        await ctx.send(embed=embed)

    @commands.command(aliases=["randomwiki", "wikirand"])
    async def wikirandom(self, ctx):
        """
        Random Wikipedia page
        """
        await ctx.channel.trigger_typing()
        search = wikipedia.search(wikipedia.random())

        page = wikipedia.page(search[0])
        title = page.title
        body = page.summary
        if len(body) >= 2000:
            body = body[:2000].rsplit(" ", 1)[0] + " **-Snippet-**"
        image = page.images[0]
        url = page.url

        embed = discord.Embed(title=title, description=body, url=url)
        embed.set_footer(text="From Wikipedia")
        embed.set_thumbnail(url=image)

        await ctx.send(embed=embed)

    @commands.command()
    async def joke(self, ctx):
        """
        They are horrible. Seriously
        """
        await ctx.channel.trigger_typing()
        req = requests.get("https://icanhazdadjoke.com", headers={"Accept": "text/plain"})
        content = req.content.decode("UTF-8")

        await ctx.send(content)

    @commands.command()
    async def norris(self, ctx):
        """
        Chuck Norris. Need I say more
        """
        await ctx.channel.trigger_typing()
        req = requests.get("https://api.chucknorris.io/jokes/random").json()["value"]
        await ctx.send(req)

    @commands.command()
    async def reddit(self, ctx, *, search):
        """
        Get a random reddit post
        """
        req = requests.get('http://reddit.com/r/' + search + '/new/.json', headers={'User-agent': 'Chrome'})
        json = req.json()
        if "error" in json or json["data"]["after"] is None:
            await ctx.send(format_error("Subreddit '{}' not found".format(search)))
            return

        req_len = len(json["data"]["children"])
        rand = random.randint(0, req_len-1)
        post = json["data"]["children"][rand]

        title = post["data"]["title"]
        author = "u/" + post["data"]["author"]
        subreddit = post["data"]['subreddit_name_prefixed']
        url = post["data"]["url"]  # can be image or post link
        link = "https://reddit.com" + post["data"]["permalink"]
        if "selftext" in post["data"]:
            text = post["data"]["selftext"]  # may not exist
            if len(text) >= 2000:
                text = text[:2000].rsplit(" ", 1)[0] + " **-Snippet-**"
            embed = discord.Embed(title=title, description=text, url=link)
        else:
            embed = discord.Embed(title=title, url=link)

        if re.match(r".*\.(jpg|png|gif)$", url):
            embed.set_image(url=url)

        embed.set_footer(text="By {} in {}".format(author, subreddit))

        await ctx.send(embed=embed)

    @commands.command()
    async def fact(self, ctx):
        """
        Fun fact. U gey
        """
        await ctx.channel.trigger_typing()
        text = requests.get("http://randomuselessfact.appspot.com/random.json?language=en").json()["text"]
        await ctx.send(text)

    @commands.command(aliases=["belikebill"])
    async def bill(self, ctx, *, name="Bill"):
        """
        Be like bill
        """
        link = "https://belikebill.ga/billgen-API.php?default=1&name=" + urllib.parse.quote(name)
        await ctx.send(embed=discord.Embed().set_image(url=link))


def setup(bot):
    bot.add_cog(Internet(bot))
