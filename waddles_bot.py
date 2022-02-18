import os
import discord
from dotenv import load_dotenv
import random
import csv
import pandas

load_dotenv()
TOKEN = os.getenv('bot_token')
GUILD = os.getenv('bot_guild')


bot_name = ""

hart_emoticon = b'\xf0\x9f\x92\x8c'.decode()
blue_emoticon = b'\xf0\x9f\x94\xa3'.decode()
check_emoticon = b'\xe2\x9c\x85'.decode()

invite_channel_name = '┃create-invite'
join_channel_name = '┃join-with-code'
check_channel_name = '┃check-invites'


full_invite_name = hart_emoticon + invite_channel_name
full_join_name = blue_emoticon + join_channel_name
full_check_name = check_emoticon + check_channel_name

all_chars = ['a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f', 'F',
              'g', 'G', 'h', 'H', 'i', 'I', 'j', 'J', 'k', 'K', 'l', 'L',
              'm', 'M', 'n', 'N', 'o', 'O', 'p', 'P', 'q', 'Q', 'r', 'R',
              's', 'S', 't', 't', 'T', 'u', 'U', 'v', 'V', 'w', 'W', 'x',
              'X', 'y', 'Y', 'z', 'Z', '1', '2', '3' , '4', '5', '6', '7',
              '8', '9']

fields = ["Name", "Code"]  ## I could add time

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(f'{client.user} has connected to Discord!')

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    bot_name = str(client.user)
    #invite_channel = await guild.create_text_channel(full_invite_name)
    #join_channel = await guild.create_text_channel(full_join_name)
    #check_channel = await guild.create_text_channel(full_check_name)

@client.event
async def on_message(message):
    global all_chars

    channel = message.channel
    #print(message.author)

    if str(message.author) != str(client.user):##name of the bot
        if str(channel) == full_invite_name:
            if message.content == "/create":
                random_code = "SC-"

                while True:
                    for _ in range(10):
                        a = random.randint(0, len(all_chars)-1)
                        random_code += str(all_chars[a])

                    print(random_code)

                    codes = []
                    f = open("generated_codes.csv", "r")
                    reader = csv.reader(f)
                    for x in reader:
                        for y in x:
                            codes.append(y)
                    if random_code not in codes:
                        break
                    
                f = open("generated_codes.csv", "a")
                csvwriter = csv.writer(f) 
                csvwriter.writerow([str(message.author), random_code]) 
                f.close()
                await channel.send(f"Your invite code is {random_code}")

        elif str(channel) == full_join_name:
            codes = []
            
            f = open("generated_codes.csv", "r")
            reader = csv.reader(f)
            
                    
            organized_codes = list(reader)
            f.close()
            organized_codes = [ele for ele in organized_codes if ele != []]
            code_found = False

            for i in range(len(organized_codes)):
                if str(organized_codes[i][1]) == message.content:
                    code_found = True

                    creator = organized_codes[i][0]
                    ##gives an extra point to the creator
                    f  = open("score_tracker.csv", "r")
                    reader = csv.reader(f)
                    organized_scores = list(reader)
                    f.close()
                    organized_scores = [ele for ele in organized_scores if ele != []]

                    inlist = False
                    place = 0
                    for i in range(len(organized_scores)):
                        if organized_scores[i][0] == creator:
                            inlist = True
                            place = i
                            break

                    if inlist == True:
                        current_score = int(organized_scores[place][1])
                        current_score += 1
                        current_score = str(current_score)
                        organized_scores[place][1] = current_score

                    else:
                        organized_scores.append([creator, "1"])

                    f  = open("score_tracker.csv", "w")
                    writer = csv.writer(f)
                    writer.writerows(organized_scores)
                    f.close()
                        
                        
                    
                    del organized_codes[i]

                    f  = open("generated_codes.csv", "w")
                    writer = csv.writer(f)
                    writer.writerows(organized_codes)
                    f.close()
                    
                    break

            if code_found == True:
                print("you're in!!!")
                await channel.send("[+] You're in!!!")

                     
            else:
                await channel.send("[-] Code is not valid")

        elif str(channel) == full_check_name:
            if (message.content).lower() == "check invites":
                print("checking invites")

                f = open("score_tracker.csv", "r")
                reader = csv.reader(f)
                organized_scores = list(reader)
                f.close()
                organized_scores = [ele for ele in organized_scores if ele != []]

                invited = False
                for i in range(len(organized_scores)):
                    if organized_scores[i][0] == str(message.author):
                        await channel.send(f"You have currently invited {organized_scores[i][1]} qualified users")
                        invited = True
                        break

                if invited == False:
                    await channel.send(f"Sorry, I couldn't find any qualified users :(")

            




client.run(TOKEN)
