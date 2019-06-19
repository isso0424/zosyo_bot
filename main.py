import discord
import requests
import lxml.html
from selenium.webdriver import Chrome
from selenium import webdriver
client = discord.Client()
TOKEN = ''
@client.event
async def on_ready():
    channel = client.get_channel()
    await channel.send("ログインしました\n?helpでコマンド一覧を取得します\nコマンドは?のあとに入力してください")

@client.event
async def on_message(message):
    # 「おはよう」で始まるか調べる
    if message.content.startswith("?"):
        # 送り主がBotだった場合反応したくないので
        if client.user != message.author:
            # メッセージを書きます
            mess = message.content[1:]
            mess = mess.split()
            print(mess)
            if mess[0] == 'book':
                await message.channel.send("蔵書一覧を表示します")
                r = requests.get("https://isso4129.pythonanywhere.com/registration/book_list")
                html = lxml.html.fromstring(r.text)
                await message.channel.send('蔵書をロード中です...')
                #蔵書分
                books = html.xpath('//*[@id="conteiner"]/div/div/div/table[1]/thead[2]/tr')
                print(books)
                book_list = []
                for books in range(1, len(books) + 1):
                    book_list.append(html.xpath('//*[@id="conteiner"]/div/div/div/table[1]/thead[2]/tr['+str(books)+']/th[1]')[0].text)
                if book_list:
                    await message.channel.send("蔵書一覧")
                book = "\n".join(book_list)
                await message.channel.send(book)
            elif mess[0] == 'rent':
                book = mess.pop(1)
                print(book)
                user = str(message.author.name)
                print(user)
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                driver = Chrome(options=options)
                driver.get('https://isso4129.pythonanywhere.com/registration/regi')
                driver.find_element_by_xpath('//*[@id="id_book"]').send_keys(book)
                driver.find_element_by_xpath('//*[@id="id_user"]').send_keys(user)
                driver.find_element_by_xpath('//*[@id="conteiner"]/div/table/tbody[2]/tr/td/input').click()
                driver.quit()
                await message.channel.send('貸出処理が完了しました\n?bookで借りられているか確認してください')
            elif mess[0] == 'return':
                book = mess.pop(1)
                print(book)
                user = str(message.author.name)
                print(user)
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                driver = Chrome(options=options)
                driver.get('https://isso4129.pythonanywhere.com/registration/rebot')
                driver.find_element_by_xpath('//*[@id="id_book"]').send_keys(book)
                driver.find_element_by_xpath('//*[@id="conteiner"]/div/div/table/tbody[2]/tr/td/input').click()
                driver.quit()
                await message.channel.send('返却処理が終わりました')
            elif mess[0] == 'c_reserv':
                r = requests.get("https://isso4129.pythonanywhere.com/registration/book_list")
                html = lxml.html.fromstring(r.text)
                await message.channel.send('蔵書をロード中です...')
                #蔵書分
                books = html.xpath('//*[@id="conteiner"]/div/div/div/table[2]/thead[2]/tr')
                print(books)
                book_list = []
                for books in range(1, len(books) + 1):
                    book_list.append(html.xpath('//*[@id="conteiner"]/div/div/div/table[1]/thead[2]/tr['+str(books)+']/th[1]')[0].text)
                if book_list:
                    await message.channel.send("予約一覧")
                book = "\n".join(book_list)
                await message.channel.send(book)
            elif mess[0] == 'borrow':
                r = requests.get("https://isso4129.pythonanywhere.com/registration/home")
                html = lxml.html.fromstring(r.text)
                await message.channel.send('蔵書をロード中です...')
                #蔵書分
                books = html.xpath('//*[@id="conteiner"]/div[2]/div[1]/table/thead[2]/tr')
                print(books)
                book_list = []
                for books in range(1, len(books) + 1):
                    book_list.append(html.xpath('//*[@id="conteiner"]/div[2]/div[1]/table/thead[2]/tr['+str(books)+']/th[1]')[0].text)
                if book_list:
                    await message.channel.send("貸出一覧")
                book = "\n".join(book_list)
                await message.channel.send(book)
            elif mess[0] == 'reservation':
                r = requests.get("https://isso4129.pythonanywhere.com/registration/home")
                html = lxml.html.fromstring(r.text)
                await message.channel.send('蔵書をロード中です...')
                # 蔵書分
                books = html.xpath('//*[@id="conteiner"]/div[2]/div[2]/table/thead[2]/tr')
                print(books)
                book_list = []
                for books in range(1, len(books) + 1):
                    book_list.append(
                        html.xpath('//*[@id="conteiner"]/div[2]/div[2]/table/thead[2]/tr[' + str(books) + ']/th[1]')[
                            0].text)
                if book_list:
                    await message.channel.send("予約一覧")
                book = "\n".join(book_list)
                await message.channel.send(book)
            elif mess[0] == 'help':
                await message.channel.send('book:今ラボ内にある本を一覧で表示します\nrent:本の貸し出しを行います\nreturn:本の返却を行います\nreservation:予約している本一覧\nc_reserv:予約できる本一覧\nborrow:貸出中の本一覧')



client.run(TOKEN)