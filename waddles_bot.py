import os
import discord
from dotenv import load_dotenv
import random
import csv
from discord.ext import commands#.commands import has_permissions, MissingPermissions
#from discord import Member

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


#client = discord.Client()
client = commands.Bot(command_prefix ='.')

#@client.command(name="kick", pass_context=True)
#@has_permissions(manage_roles=True, ban_members=True)
#async def _kick(ctx, member: Member):
#    await bot.kick(member)#

#@_kick.error
#async def kick_error(ctx, error):
#    if isinstance(error, MissingPermissions):
#        text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
#        await bot.send_message(ctx.message.channel, text)

@client.command()
async def ping(ctx):
    print("biem")
    await ctx.send("pong")



@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    guild = client.get_guild(guild.id)
    for x in guild.members:
        print(x)
    print(f'{client.user} has connected to Discord!')

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    bot_name = str(client.user)

    ##perms = discord.Permissions(send_messages=False, read_messages=True)
    ##await client.create_role(server, name='NoSend', permissions=perms)

    
    #invite_channel = await guild.create_text_channel(full_invite_name)
    #join_channel = await guild.create_text_channel(full_join_name)
    #check_channel = await guild.create_text_channel(full_check_name)
    
    #print(channel)
    #print(discord.Permissions(5))


    
@client.event
async def on_message(message):
    global all_chars

    channel = message.channel
    print(message.author)
    #member = message.author

    #var = discord.utils.get(message.guild.roles, name = "new_role")
    #member.add_role(var)

    #server = ctx.message.server
    #perms = discord.Permissions(send_messages=False, read_messages=True)
    #await client.create_role(server, name='NoSend', permissions=perms)


    
    if message.author.guild_permissions.administrator:
        print("the user is admin")
    else:
        print(message.author.guild_permissions.administrator)


    if str(message.author) != str(client.user):##name of the bot
        if str(channel) == full_invite_name:
            print("biem")
            if message.content == "/create":
                ##checks if the code is already generated
                f = open("generated_codes.csv", "r")
                reader = csv.reader(f)
                organized_codes = list(reader)
                f.close()
                organized_codes = [ele for ele in organized_codes if ele != []]


                code_created = False
                for i in range(len(organized_codes)):
                    print(organized_codes[i][0])
                    if str(organized_codes[i][0]) == str(message.author):
                        code_created = True
                        generated_code = organized_codes[i][1]
                        break
                    

                if code_created == False:
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

                elif code_created == True:
                    await channel.send(f"Your already generated code is {generated_code}")

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
                    if str(message.author) != organized_codes[i][0] or str(message.author) == "fluflu#2539" or str(message.author) == "SUPERCOCO_NFT": 
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
                            ##checks if the score is >= 10
                            if organized_scores[place][2] == "0" and current_score >= 10:
                                organized_scores[place][2] = "1"
                                ##adds the creator to the "Member" role
                                member = channel.guild.get_member_named(creator)
                                #if member == None:
                                #    member = message.author
                                role = discord.utils.get(member.guild.roles, name="BE MEMBERS")
                                await member.add_roles(role)
                                print("added the creator to the 'BE MEMBERS' role")
                                
                            current_score = str(current_score)
                            organized_scores[place][1] = current_score

                        else:
                                                    ##name, score, member(0 == False)
                            organized_scores.append([creator, "1", "0"])
                            #await channel.send("Con

                        f  = open("score_tracker.csv", "w")
                        writer = csv.writer(f)
                        writer.writerows(organized_scores)
                        f.close()
                            
                            
                        
                        #del organized_codes[i]

                        f  = open("generated_codes.csv", "w")
                        writer = csv.writer(f)
                        writer.writerows(organized_codes)
                        f.close()
                        
                        break

                    else:
                        await channel.send("You cannot invite yourself")
                        return
                        
            if code_found == True:
                await channel.send("[+] You're in!!!")

                    
                
            else:
                await channel.send("[-] Code is not valid")

        elif str(channel) == full_check_name:
            if (message.content).lower() == "/invites":
                print("checking invites")

                f = open("score_tracker.csv", "r")
                reader = csv.reader(f)
                organized_scores = list(reader)
                f.close()
                organized_scores = [ele for ele in organized_scores if ele != []]

                for i in range(len(organized_scores)):
                    if organized_scores[i][0] == str(message.author):
                        print(organized_scores[i][1])
                        await channel.send(f"You have currently invited {organized_scores[i][1]} qualified users")
                        if organized_scores[i][2] == "1":
                            await channel.send(f"So You are a BE MEMBER")
                        break
                    
                ##if he ended the loop, it means that you don't have any invites yet
                await channel.send("You don't have invited any users yet")


client.run(TOKEN)
