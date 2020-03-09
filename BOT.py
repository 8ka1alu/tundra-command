import datetime
import subprocess
import numpy as np
import os
import discord
import math
from discord.ext import commands
import sqlite3

def makefactor(x: int) -> list:
    """
    Return factors list of x. Raise ValueError if x is 0 or 1.
    """
    if x == 0 or x == 1:
        raise ValueError
    f_ls = []
    i = 2
    while i < x:
        if x % i == 0:
            f_ls.append(i)
            i += 1
            continue
        else:
            i += 1
            continue
    return f_ls


bot = commands.Bot(command_prefix='n')
bot.remove_command('help')
token = os.environ['DISCORD_BOT_TOKEN']
loaded = datetime.datetime.now(
    datetime.timezone(datetime.timedelta(hours=9))
)
loaded = loaded.strftime('%Y年%m月%d日 %H:%M')

# ここからコマンド

# ヘルプコマンド。コマンドを追加した場合、周りに従って追記すること。
@bot.command()
async def help(ctx, tohelp='all'):  # tohelpにはヘルプを表示するコマンド名が入る
    if tohelp == 'all':
        embed = discord.Embed(title='現在利用可能なコマンドは以下のとおりです。', description='', color=0xffffff)
        embed.add_field(name='ncheck', value='このBotがオンラインがどうか確認できます。Botの反応がないときにお使いください。', inline=False)
        embed.add_field(name='nsay', value='任意のテキストを送信します。', inline=False)
        embed.add_field(name='nisprime', value='素数かどうか判定します。数値以外の入力には対応していません。', inline=False)
        embed.add_field(name='ncalc', value='BOTに計算させることができます。Pythonの標準機能を使用するため、高度なことはできません。', inline=False)
        embed.add_field(name='npython', value='Pythonのコマンドを実行し、実行結果を返します。', inline=False)
        
        # nhelpの説明は一番最後に
        embed.add_field(name='nhelp', value='この一覧を表示します。', inline=False)
        await ctx.send(embed=embed)
    if tohelp == 'check':
        embed = discord.Embed(title='使用方法 ： `ncheck`', description='Botが現在オンラインかどうかを確認できます。\nBotの反応がないときにお使いください。', inline=False, color=0xffffff)
        await ctx.send(embed=embed)
    if tohelp == 'say':
        embed = discord.Embed(title='使用方法 ： `nsay (delete) <文字列>`', description='BOTに任意の文字列を送信させることができます。\n文字列の前にdeleteを入れることにより、本当にBOTが話しているように見せることもできます。', color=0xffffff)
        await ctx.send(embed=embed)
    if tohelp == 'isprime':
        embed = discord.Embed(title='使用方法 ： `nisprime <数値>`', description='素数かどうか判定します。数値以外の入力には対応していません。', color=0xffffff)
        await ctx.send(embed=embed)
    if tohelp == 'calc':
        embed = discord.Embed(title='使用方法 ： `ncalc <式>`', description='BOTに計算させることができます。', color=0xffffff)
        await ctx.send(embed=embed)
    if tohelp == 'python':
        embed = discord.Embed(title='使用方法 ： `npython <コマンド>', description='Pythonのコマンドを実行し、実行結果を返します。', color=0xffffff)
        await ctx.send(embed=embed)
    

@bot.command()
async def check(ctx):
    await ctx.send("このBotは現在稼働中です。\n最終更新日時は" + loaded + 'です。')


@bot.command()
async def say(ctx, *, message='使用方法 ： `nsay 文字列`'):
    if message.startswith('delete') == True:
        await discord.ext.commands.bot.discord.message.Message.delete(ctx.message)
        message = message.split()
        message[0] = ''
        message = ' '.join(message)
        message = message.strip()

    await ctx.send(message)


@bot.command()
async def isprime(ctx, *, message='0'):
    returning = '入力が不適切です:自然数を入力して下さい'
    is_composite = False
    if message.isdecimal() == True:
        num = int(message)
        if num < 2 or (num % 2 == 0 and num > 2):
            returning = str(num) + 'は素数ではありません'
        else:
            lim = int(math.sqrt(num)) + 1
            for i in range(3, lim, 2):
                if num % i == 0:
                    is_composite = True
                    break
            if is_composite:
                returning = str(num) + 'は素数ではありません'
            else:
                returning = str(num) + 'は素数です'
        await ctx.send(returning)
    else:
        await ctx.send(returning)


@bot.command()
async def mkf(ctx, *, message='0'):
    global factors
    error = "入力が不適切です:自然数を入力して下さい"
    if message.isdecimal() == True:
        try:
            factors = makefactor(int(message))
        except ValueError:
            await ctx.send(error)
        factors = ', '.join(map(str, factors))
        await ctx.send(factors)


@bot.command()
async def calc(ctx, *, formula):
    await ctx.send(str(eval(formula)))


@bot.command()
async def python(ctx, *, toexe='print("コマンドを入力してください")'):
    global endline, endline
    DoAlthoughOver2000 = toexe.startswith('-full')
    if DoAlthoughOver2000 == True:
        toexe = toexe.split(None, 1)
        if len(toexe) >= 2:
            toexe = toexe[1]
        else:
            toexe = 'print("コマンドを入力してください")'

    with open("temp.py", "w") as f:
        print(toexe, file=f)

    result = subprocess.run(
        'python temp.py', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    result = result.stdout.decode('utf-8')
    if len(result) + 6 >= 2000:
        if DoAlthoughOver2000 == True:
            result = result.splitlines()
            i = 1
            startline = 0
            for i in range(1, len(result) + 1):
                temp = result[startline:i]
                temp = '\n'.join(temp)
                if len(temp) + 6 >= 2000:
                    endline = i - 1
                    content = result[startline:endline]
                    content = '```\n' + '\n'.join(content) + '\n```'
                    startline = endline + 1
                    await ctx.send(content)
                else:
                    endline = i
            content = result[startline:endline]
            content = '```\n' + '\n'.join(content) + '\n```'
            await ctx.send(content)
        else:
            await ctx.send('出力された文字数が2000を超えています。続行するには`-full`オプションをつけてください。')
    else:
        result = '```\n' + result + '\n```'
        await ctx.send(result)
          
@bot.group()
async def mp(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('このコマンドにはサブコマンドが必要です。')


@mp.command()
async def create(ctx,what):
    conn = sqlite3.connect('discordbot.db')
    c = conn.cursor() 
    c.execute(f"CREATE TABLE {what} ({what} TEXT, price INTEGER)")
    await ctx.send("登録しました。")
    conn.commit()
    conn.close()

# 接続
bot.run(token)

