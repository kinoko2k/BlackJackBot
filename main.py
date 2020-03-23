import asyncio
import random
import traceback
from datetime import datetime

import discord
from discord import Embed

client = discord.Client()


@client.event
async def on_ready():
    print("-----------------------------")
    print("|        version: 1.0       |")
    print("| Created by soundofhorizon |")
    print("|        Bot is Ready!      |")
    print("-----------------------------")


@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    try:
        if message.content == "!bj":
            # cardIndex.txtに書かれたファイル名を読み込んでListへ
            card_data = open("card/cardIndex.txt", "r")
            lines = card_data.readlines()
            card_data.close()
            score = 0
            score_low = 0
            score_high = 0

            # 各自ファイル名に対してスコアを決定
            def score_calc(m):
                if m == "2 (1).png" or m == "2 (2).png" or m == "2 (3).png" or m == "2 (4).png":
                    return 2
                elif m == "3 (1).png" or m == "3 (2).png" or m == "3 (3).png" or m == "3 (4).png":
                    return 3
                elif m == "4 (1).png" or m == "4 (2).png" or m == "4 (3).png" or m == "4 (4).png":
                    return 4
                elif m == "5 (1).png" or m == "5 (2).png" or m == "5 (3).png" or m == "5 (4).png":
                    return 5
                elif m == "6 (1).png" or m == "6 (2).png" or m == "6 (3).png" or m == "6 (4).png":
                    return 6
                elif m == "7 (1).png" or m == "7 (2).png" or m == "7 (3).png" or m == "7 (4).png":
                    return 7
                elif m == "8 (1).png" or m == "8 (2).png" or m == "8 (3).png" or m == "8 (4).png":
                    return 8
                elif m == "9 (1).png" or m == "9 (2).png" or m == "9 (3).png" or m == "9 (4).png":
                    return 9
                else:
                    return 10

            showFileURI1 = lines[random.randint(0, 51)].replace('\n', '')
            if showFileURI1 == "A (1).png" or showFileURI1 == "A (2).png" or showFileURI1 == "A (3).png" or showFileURI1 == "A (4).png":
                score_low += 1
                score_high += 11
            else:
                score_low += score_calc(showFileURI1)
                score_high += score_calc(showFileURI1)

            showFileURI2 = lines[random.randint(0, 51)].replace('\n', '')
            if showFileURI2 == "A (1).png" or showFileURI2 == "A (2).png" or showFileURI2 == "A (3).png" or showFileURI2 == "A (4).png":
                score_low += 1
                # 高いほうのスコアが21を超えるかどうかの判断を行う。Aが2枚あったとき、現時点でlow8.high19だとして、+1は耐える
                if score_high + 11 > 21 and score_high + 1 < 21:
                    score_high += 1
                else:
                    score_high += 11
            else:
                score_low += score_calc(showFileURI2)
                score_high += score_calc(showFileURI2)

            my_files = [
                discord.File(f'card/{showFileURI1}'),
                discord.File(f'card/{showFileURI2}'),
            ]
            await message.channel.send(files=my_files)

            if score_low == score_high or score_high > 21:
                await message.channel.send(f"**{message.author.display_name}'s Score is: {score_low}**")
            else:
                if score_high == 21:
                    await message.channel.send("_**BlackJack!!**_")
                    return
                await message.channel.send(
                    f"**{message.author.display_name}'s Score is: low:{score_low}, high:{score_high}**")

            await message.channel.send("HIT? or STAND? please write your action -> ['hit', 'stand']")

            # 書いた人がコマンド打った人、また、standかhitを打った人
            def check(m):
                return m.author.id == message.author.id and m.content == 'stand' or m.content == 'hit'

            try:
                # ユーザーの返答を待つ
                playerSelect = await client.wait_for('message', check=check, timeout=60.0)

                # standじゃない分、カード引き続けてどうぞ

                while playerSelect != "stand":
                    if playerSelect.content == "hit":
                        addFileURI = lines[random.randint(0, 51)].replace('\n', '')

                        if addFileURI == "A (1).png" or addFileURI == "A (2).png" or addFileURI == "A (3).png" or addFileURI == "A (4).png":
                            score_low += 1
                            # 高いほうのスコアが21を超えるかどうかの判断を行う。Aが2枚あったとき、現時点でlow8.high19だとして、+1は耐える
                            if score_high + 11 > 21 and score_high + 1 < 21:
                                score_high += 1
                            else:
                                score_high += 11
                        else:
                            score_low += score_calc(addFileURI)
                            score_high += score_calc(addFileURI)

                        await message.channel.send(file=discord.File(f'card/{addFileURI}'))

                        # Aの最大値が21超えた時
                        if score_low == score_high or score_high > 21:
                            if score_low == 21:
                                await message.channel.send("_**Just 21!**_")
                                return
                            await message.channel.send(f"**{message.author.display_name}'s Score is: {score_low}**")
                        else:
                            if score_high == 21:
                                await message.channel.send("_**Just 21!**_")
                                return
                            await message.channel.send(
                                f"**{message.author.display_name}'s Score is: low:{score_low}, high:{score_high}**")

                        if score_low > 21:
                            await message.channel.send("You are **BURST!!!!!!!!!**")
                            return

                        await message.channel.send("HIT? or STAND? please write your action -> ['hit', 'stand']")
                        playerSelect = await client.wait_for('message', check=check, timeout=60.0)

                    elif playerSelect.content == "stand":
                        # Aが出た時、高い点だった場合はこのスコアを採用するだろう。
                        if score_high != 0 and score_high <= 21:
                            score = score_high
                        elif score_low != 0:
                            score = score_low

                        await message.channel.send(f"**{message.author.display_name}'s Score is: {score}**")
                        return

            except asyncio.TimeoutError:
                await message.channel.send("You are Timeout! BURST!")

        if message.content == "!bj_help":
            await message.channel.send("自分の得点を**21**に近づけろ…超えるんじゃねえぞ…", file=discord.File("help/explain.png"))

    except:
        error_message = f'```{traceback.format_exc()}```'
        ch = message.guild.get_channel(691239648277692476)
        d = datetime.now()  # 現在時刻の取得
        time = d.strftime("%Y/%m/%d %H:%M:%S")
        embed = Embed(title='Error_log', description=error_message, color=0xf04747)
        embed.set_footer(text=f'channel:{message.channel}\ntime:{time}\nuser:{message.author.display_name}')
        await ch.send(embed=embed)


client.run("TOKEN")