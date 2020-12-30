from discord.ext import commands
from random import randrange, shuffle
import nest_asyncio
import discord
import gspread 
from oauth2client.service_account import ServiceAccountCredentials 
import asyncio
import pandas as pd
from gspread_dataframe import set_with_dataframe
from tabulate import tabulate

credentials = {
  "type": "service_account",
  "project_id": "python-db-299500",
  "private_key_id": "5d23e6fed9467d50686cddb6af53094cfef725cb",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDE5EOdBdyBjtzM\nQR/7GvVikHmCRcgSuVFkoG4CWJYfxc/766qqdUnbLmcSBsxETGPVEAUfs1fObQWV\nMd6s93aqihrUgCDhThw4df94wXC8YugjTExSTGa2dItzPhs57lHFbM82aPUwslQ2\nJMYKBlDBA1IbhTEN0/E6UaT0nq7ROv/hmX6ry2IN21VlcIlfwJOILRcznu9/0CLK\nvhW3W/Se2EeqT+QK3kg4amjTBh5Ka/QA+yF+W3LczqneLCr8Rz/FGrbchHMf59W7\nkxT/RPv1orrgLXWVnq+Gr9kZEuBOGxo5RThlOfKo/YS/Bfa9F7zmD0me07gkv2yC\n73MhDYGvAgMBAAECggEAAnv/+i+ilLXsmsC+gYGu2qOW1Aa1DWmnGYuPknaPze63\n4oLwB2lfIF5+zQDt9JH/vnwAblPNm1VeDn/viWsT84V9Xp9k0e2jjdqbTyGYZYOx\nwdYKyvCbhZ/3LWHrLlzIos1f2KQUENYuUmYhnHlTl9zGsp5PkYjutAQufkcGFgNs\n9OtYtpJvXwaIKNfjKYOJBOU8RbqRZ+P36ZbvwkRQVEmX/D/SaPpKR8PNxwyIqpi/\n2ylwacJjGmImh+h6UuwyPNjCU6tGB1xPEkNf6c7zfhloGKZwTMTeh4Hnhu3dfhbE\nY/4BKFLiSZQnZgSGhOad4Tb1Fkzh+tUTHv9zALRxoQKBgQDn+D7vn5769/KWr89+\ndtM1xiZXRjVsIJ6PttHH1AiAi+FDJNx8hIuwJOKscsiXWeRm7Me2SJT5xiia+yVw\npBDBPyP28btzn+em5F+cwRiXz3LRXNa54ME8vbAMA0iPucPMBmJOwYPBiYmzii8B\nPBGvcb5orQ+VhQNWm5ec7hrs4QKBgQDZScLCDJeIXBeJVFtepUsJUUNJxHXWVUq2\nAdwZO2CLz6Os1xmqLe3VgnOrU4DGhDjZG0xm+CnJFL9DaQAEd3TS2f8xKEGIaQoT\ndJn4R+GE0/U0ZSCblYu28lkIl4ju2r18/AVrCvELkqYqEdRvxh6g3Q3DO0gvTS6f\n/EB/hbkwjwKBgQCo2XI2SiIW3FSgiuimTSgAhHN0I47PXg8M3S5mHljx+N/HWBWG\nLZTganj0vbh1MuGmacQVU0/dX/g+l4DxNPtdLvCm195yk3qzaJiQKZ4VItOYwdMr\nCgaeiBSVKe6vb7Ct2hfE6+dUASFSpssAQxE8e7b1ysMFOwTrDeaWPFstAQKBgQDF\nJX2FnvMmD5hzS4yTNRn93DNXDN91lnFw7gMLCaqxb7WrroZkt8Ngwzm7qsneVD1Y\nDsKlcmhHP4HB4dTYOKJQZOZ7bXD4GYXA3TyN3nopkD6cSVzqjSb02LIbb5IYVXMz\noV4xHv5RZ79H0GGVAIbtoWNJTdJSyI6TLcY/bc721QKBgQC4LyR1f0CFj+wlXR+C\neoBc2C2qkW3FR1HV7or0TxDGRSUnNomnW7AZqAgunhRlRpgv4t0WKM31rDgxxpO4\nzJvgv2C1xk/S3x4hJa5N0GDp11oXtmWQ4Am0ZiDdG5YO+XpKHWxoc00mRRfKOQOs\ngUy6BQVoJIIC9u0U4ITWfFWPhg==\n-----END PRIVATE KEY-----\n",
  "client_email": "python-casino-bot@python-db-299500.iam.gserviceaccount.com",
  "client_id": "110303608809712246077",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/python-casino-bot%40python-db-299500.iam.gserviceaccount.com"
}

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', 
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"] 
 

# Assign credentials ann path of style sheet 
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope) 
client = gspread.authorize(creds) 
sheet = client.open("Casino Bot DB").sheet1 

# Display data 
data = sheet.get_all_records()
data_pd = pd.DataFrame.from_dict(data)
data_pd["Discord ID"] = data_pd["Discord ID"].str.replace('a', '')

#Databases

# Slot Machine
slot_possible = ["A", "A", "A", "K", "K", "K", "K", "Q", "Q", "Q", "Q", "Q", "Q", "Q", "J", "J", "J", "J", "J", "J", "J", "J", "J", "10", "10", "10", "10", "10", "10", "10", "7"]
slot_multi = {"7": 100, "A": 25, "K": 15, "Q": 10, "J": 8, "10": 5}
slot_multi2 = {"7": 30, "A": 10, "K": 5, "Q": 3, "J": 2, "10": 1}

# Roulette Stuff
number = False
index = None
nome = None
list_players = data_pd['Discord ID'].tolist()
roulette_spin = 0
routette_bets_allow = 0
roulette_in_calc = 0


win_result_round = []
lose_result_round = []
historic = []
data_rank = []

def chip_count(user_id):
    return data_pd.loc[data_pd['Discord ID'] == str(user_id), "Chips"].iloc[0]

def true_spin():
    global roulette_spin
    roulette_spin = 1

def true_allow_bets():
    global routette_bets_allow
    routette_bets_allow = 1
    
def false_spin():
    global roulette_spin
    roulette_spin = 0

def false_allow_bets():
    global routette_bets_allow
    routette_bets_allow = 0

def true_calc():
    global roulette_in_calc
    roulette_in_calc = 1

def false_calc():
    global roulette_in_calc
    roulette_in_calc = 0
    

roulette_dict = {"0": ["https://i.imgur.com/6gNoj11.png", "Green", "Green", ":green_circle:", "Green"], "1": ["https://i.imgur.com/5t8O8sP.png", "Red", "Odd", ":red_circle:", "T1"],
                 "2": ["https://i.imgur.com/YemZ7DR.png","Black","Even", ":black_circle:", "T1"], "3": ["https://i.imgur.com/YSHB35I.png","Red","Odd", ":red_circle:", "T1"],
                 "4": ["https://i.imgur.com/YcHi8Ty.png","Black","Even", ":black_circle:", "T1"], "5": ["https://i.imgur.com/P55otdV.png","Red","Odd", ":red_circle:", "T1"],
                 "6": ["https://i.imgur.com/6V0ehHa.png","Black","Even", ":black_circle:", "T1"], "7": ["https://i.imgur.com/haLsfOu.png","Red","Odd", ":red_circle:", "T1"],
                 "8": ["https://i.imgur.com/RlX6k8P.png","Black","Even", ":black_circle:", "T1"], "9": ["https://i.imgur.com/N3U19NM.png","Red","Odd", ":red_circle:", "T1"],
                 "10": ["https://i.imgur.com/MESSNAr.png","Black","Even", ":black_circle:", "T1"], "11": ["https://i.imgur.com/qaglXAE.png","Black","Odd", ":black_circle:", "T1"],
                 "12": ["https://i.imgur.com/uCk5qf3.png","Red","Even", ":red_circle:", "T1"], "13": ["https://i.imgur.com/SuKttnL.png","Black","Odd", ":black_circle:", "T2"],
                 "14": ["https://i.imgur.com/3zqHa47.png","Red","Even", ":red_circle:", "T2"], "15": ["https://i.imgur.com/seBxCQj.png","Black","Odd", ":black_circle:", "T2"],
                 "16": ["https://i.imgur.com/3RNcwT1.png","Red","Even", ":red_circle:", "T2"], "17": ["https://i.imgur.com/xQZGkyh.png","Black","Odd", ":black_circle:", "T2"],
                 "18": ["https://i.imgur.com/CfG8UHP.png","Red","Even", ":red_circle:", "T2"], "19": ["https://i.imgur.com/rEyXlem.png","Red","Odd", ":red_circle:", "T2"],
                 "20": ["https://i.imgur.com/AOeQclf.png","Black","Even", ":black_circle:", "T2"], "21": ["https://i.imgur.com/FLjqErT.png","Red","Odd", ":red_circle:", "T2"],
                 "22": ["https://i.imgur.com/cnqxin9.png","Black","Even", ":black_circle:", "T2"], "23": ["https://i.imgur.com/6TdT0Vq.png","Red","Odd", ":red_circle:", "T2"],
                 "24": ["https://i.imgur.com/O4uaIAW.png","Black","Even", ":black_circle:", "T2"], "25": ["https://i.imgur.com/bjNaHa7.png","Red","Odd", ":red_circle:", "T3"],
                 "26": ["https://i.imgur.com/N7mlNbx.png","Black","Even", ":black_circle:", "T3"], "27": ["https://i.imgur.com/KxzBWB3.png","Red","Odd", ":red_circle:", "T3"],
                 "28": ["https://i.imgur.com/BvMjyRD.png","Black","Even", ":black_circle:", "T3"], "29": ["https://i.imgur.com/FAQr09M.png","Black","Odd", ":black_circle:", "T3"],
                 "30": ["https://i.imgur.com/X8OIwbV.png","Red","Even", ":red_circle:", "T3"], "31": ["https://i.imgur.com/RR9wbFm.png","Black","Odd", ":black_circle:", "T3"],
                 "32": ["https://i.imgur.com/AR2bYKW.png","Red","Even", ":red_circle:", "T3"], "33": ["https://i.imgur.com/U8AuALD.png","Black","Odd", ":black_circle:", "T3"],
                 "34": ["https://i.imgur.com/tfXbKeP.png","Red","Even", ":red_circle:", "T3"], "35": ["https://i.imgur.com/yhHMaUq.png","Black","Odd", ":black_circle:", "T3"],
                 "36": ["https://i.imgur.com/W0fVMlj.png","Red", "Even", ":red_circle:", "T3"]}


statements_dict = {"$help": "```fix\n$games - See all the available Games\n$mychips - Your Current Chip Count\n$prizes - See the prizes you can redeem with your chips!\n$rules - See further information about Chips and Games\n$rank - See how you fare against your opponents (Leaderboard)```",
                    "$games": "```fix\nRoullete - $roulette\nSlot Machine - $slot```",
                    "$rules": "```fix\nEveryhour you receive 5 free chips in your Account! When you have enough Chips you can redeem your Prize near One Lider Boi! Enjoy!\nSee prizes with $prizes```",
                    "$prizes": "```fix\n5.000 Chips: Escolhe o que Alceo BANE e PICKA num jogo de LoL\n10.000 Chips: Joker para o Gameshow da PDA\n200.000 Chips: Torna-te Mod do Server!\n500.000 Chips: Cria o teu Text Channel aqui no Discord\n1.000.000 Chips: 10 Euros (cash) ```",
                    "$roulette": "```fix\nWelcome to the LIDL Roulette!\nFirst please Spin the roulette with $rspin! When the Roulette is spinning place as many bets as you please, using: $rbet [type of bet] [amount of chips]\n\nTypes of Bets: Number (Pays 1-36), Thirds [t1, t2, t3] (Pays 1-3), Red/Black (Pays 1-2), Even/Odd (Pays 1-2)\n\nExamples: $rbet Black 10 (Bets 10 Chips on Black);\n$rbet 1 5 (Bets 5 Chips on number 5)```",
                    "$slot": "```To use the slot, type the command: $sbet [number of lines] [amount of chips]. Number of lines can only be 1, 3 or 5, the more lines you choose the more opportunities you have to win!\nThe Total Amount Betted = Number of Lines x Amount Chips```\nWinning Combinations Must ALWAYS Start in the 1st column!\nhttps://i.imgur.com/DGATqNN.png"}

possible = ["black", "red", "even", "odd", "t1", "t2", "t3"]

for values in range(0, 37):
    possible.append(str(values))

# Program

nest_asyncio.apply()

Client = discord.Client()
client = commands.Bot(command_prefix = "$")

@client.event
async def on_ready():
    channel = client.get_channel(792218612445478932)
    await channel.send("```fix\nHello Fellow Gamblers!\nThis is Casino Bot Sponsored by LIDL!  \n \nType $help to see the available Games, Prizes and your current Chip Count\n\nEnjoy your Gamling, have Fun !```")
    print("Bot is online and connected to Discord")
    
    for timeeee in range(0, 10000000):
        data_pd["Chips"] = data_pd["Chips"] + 5
        data_pd["Discord ID"] = data_pd["Discord ID"] + "a"
        set_with_dataframe(sheet, data_pd)
        data_pd["Discord ID"] = data_pd["Discord ID"].str.replace('a', '')
        await asyncio.sleep(360)

# $Roulette
@client.event

async def on_message(message):
    
    channel = client.get_channel(792218612445478932)
    user_id = message.author.id
    
    if message.channel.name == "🎰lidl-casino" and str(user_id) in list_players:
        if roulette_in_calc == 1:
            await channel.send("Please you need to bet farther apart from the other players, try again", delete_after = 10)            
            
        else: 
            
            if message.content == "$rspin":
                if roulette_spin == 1:
                    await channel.send("The Roulette is already spinniiiiiing Babyy!!", delete_after = 5)
                    
                else:  
                    true_spin()
                    true_allow_bets()
                    
                    await channel.send("```fix\nSpin. The. Rouletteeeee!!!\n\nPlease place your bets!```", delete_after = 30)
                    await channel.send("https://i.imgur.com/bX8ZlOy.gif", delete_after = 30)
                    number = randrange(37)
                    global outcome
                    outcome = [str(number), roulette_dict[str(number)][1].lower(), roulette_dict[str(number)][2].lower(), roulette_dict[str(number)][4].lower()]
                    
                    y = 1                
                    
                    if len(historic[-15:]) > 0:
                        
                        text = ""
                        total_text = ""                    
        
                        for histo in historic[-15:]:
                            text = str(y) + "# " + roulette_dict[str(histo)][3] + " "  + str(histo) + " " + roulette_dict[str(histo)][2] + "\n"
                            total_text = total_text + text                
                            y += 1                              
                        
                        await channel.send("```fix\nLast 10 Numbers:```", delete_after = 30)
                        await channel.send(total_text, delete_after = 30)
                    
                    await asyncio.sleep(30)
                    false_allow_bets()
                    await channel.send("```fix\nNo more bets```", delete_after = 10)
                    await asyncio.sleep(10)
                    false_spin()
                    
                    await channel.send(roulette_dict[str(number)][0] + "\n" + roulette_dict[str(number)][3] + " " + list(roulette_dict.keys())[number] + ", " + roulette_dict[str(number)][2] + ", " + roulette_dict[str(number)][4] + "\n", delete_after = 30)       
                    
                    global win_result_round
                    global lose_result_round
                    
                    for plays in win_result_round:
                        data_pd.iloc[plays[0], 2] = data_pd.iloc[plays[0], 2] + plays[2]
                        await channel.send("Congrats " + plays[1] + " you won: " + str(plays[2]) + " Chips!", delete_after = 20)     
                       
                    for plays1 in lose_result_round:
                        await channel.send("Damn " + plays1[1] + " you lost: " + str(plays1[2]) + " Chips :(", delete_after = 20)     
                    
                    historic.append(str(number))
                    win_result_round = []
                    lose_result_round = []                
                    outcome = []
                    number = None
            
            elif message.content.startswith("$rbet"):
                if roulette_spin == 0:
                    await channel.send("You gotta spin the roulette first!\n\n Use the command: $rspin", delete_after = 10)     
                elif routette_bets_allow == 0:
                    await channel.send("No more Bets allowed!", delete_after = 15)                     
                elif len(message.content.split()) != 3:
                    await channel.send("Misscliked?\nExample format: $rbet black 10 [command, type, bet amount]", delete_after = 10)
                elif (message.content.split()[1]).lower() not in possible:
                    await channel.send("Wrong Bet type!\n\nAvailable Bets: (Red, Black), (Odd, Even), Thirds (t1, t2, t3), Numbers (0 - 36)", delete_after = 10)
                elif message.content.split()[2].isdigit() == False:
                    await channel.send("\nWe only take FULL chips!", delete_after = 10)
                elif int(message.content.split()[2]) > chip_count(user_id):
                    await channel.send("Hey you don't have that amount of chips!\nYou currently only have: " + str(chip_count(user_id)) + " chips", delete_after = 10)            
                    
                else:
                    true_calc()
                    global index
                    global nome
                    better = message.author.id
                    index = data_pd.loc[data_pd['Discord ID'] == str(better)].index[0]
                    nome = data_pd.loc[data_pd['Discord ID'] == str(better), "Name"].iloc[0]
                  
                    data_pd.iloc[index, 2] = data_pd.iloc[index, 2] - int(message.content.split()[2])
                    data_pd.iloc[index, 3] = data_pd.iloc[index, 3] + 1
                    await channel.send("Aposta Válida", delete_after = 2)            
                    
                    if message.content.split()[1].isdigit() == True and message.content.split()[1] in outcome:
                        win_result_round.append([index, nome, int(message.content.split()[2]) * 36])
                    
                    elif message.content.split()[1].startswith("t") and message.content.split()[1].lower() in outcome:
                        win_result_round.append([index, nome, int(message.content.split()[2]) * 3])                    
                    
                    elif message.content.split()[1].lower() in outcome:
                        win_result_round.append([index, nome, int(message.content.split()[2]) * 2])
    
                    else:
                        lose_result_round.append([index, nome, int(message.content.split()[2])])
                    
                    false_calc()
                    
                    
            if message.content.startswith("$sbet"):
                if len(message.content.split()) != 3 or message.content.split()[1].isdigit() == False or message.content.split()[2].isdigit() == False or message.content.split()[1] not in ["1", "3", "5"]:
                    await channel.send("Wrong Format. Please use: $sbet [number of lines] [amount of chips]. Number of lines can only be 1, 3 or 5!", delete_after = 10)
                
                elif int(message.content.split()[2]) > chip_count(user_id):
                    await channel.send("Hey you don't have that amount of chips!\nYou currently only have: " + str(chip_count(user_id)) + " chips", delete_after = 10)            

                else:
                    true_calc()
                    
                    better = message.author.id
                    index = data_pd.loc[data_pd['Discord ID'] == str(better)].index[0]
                    nome = data_pd.loc[data_pd['Discord ID'] == str(better), "Name"].iloc[0]
                    
                    total_betted = int(message.content.split()[2]) * int(message.content.split()[1])
                    
                    data_pd.iloc[index, 4] = data_pd.iloc[index, 4] + 1
                    await channel.send("```Machine Spinning!!```", delete_after = 2)                       
                    
                    shuffle(slot_possible)
                    p11 = slot_possible[0]
                    p21 = slot_possible[1]
                    p31 = slot_possible[2]
                    shuffle(slot_possible)
                    p12 = slot_possible[0]
                    p22 = slot_possible[1]
                    p32 = slot_possible[2]
                    shuffle(slot_possible)    
                    p13 = slot_possible[0]
                    p23 = slot_possible[1]
                    p33 = slot_possible[2]
                    wins = []
                    profit = 0
                        
                    if int(message.content.split()[1]) > 0:
                        line1 = [p21, p22, p23]
                        sline1 = [p21, p22]
                        
                        if len(set(line1)) == 1:
                            profit += slot_multi[str(line1[0])] * int(message.content.split()[2])
                            wins.append(" 3x " + str(line1[0]) + " - "  + str(slot_multi[str(line1[0])] * int(message.content.split()[2])) + " Chips |")
                            
                        elif len(set(sline1)) == 1:
                            profit += slot_multi2[str(line1[0])] * int(message.content.split()[2])
                            wins.append(" 2x " + str(line1[0]) + " - "  + str(slot_multi2[str(line1[0])] * int(message.content.split()[2])) + " Chips |")
                        
                        elif p11 == "7" or p21 == "7" or p31 == "7":
                            profit += int(message.content.split()[2])
                            if int(message.content.split()[1]) == 1:  
                                wins.append(" 1x 7 - " + str(int(message.content.split()[2])) + " Chips |")
                        
                        if int(message.content.split()[1]) > 1:
                            line2 = [p11, p12, p13]
                            line3 = [p31, p32, p33]
                            sline2 = [p11, p12]
                            sline3 = [p31, p32]   
                            
                            if len(set(line2)) == 1:
                                profit += slot_multi[str(line2[0])] * int(message.content.split()[2])
                                wins.append(" 3x " + str(line2[0]) + " - "  + str(slot_multi[str(line2[0])] * int(message.content.split()[2])) + " Chips |")
                                
                            elif len(set(sline2)) == 1:
                                profit += slot_multi2[str(line2[0])] * int(message.content.split()[2])
                                wins.append(" 2x " + str(line2[0]) + " - "  + str(slot_multi2[str(line2[0])] * int(message.content.split()[2])) + " Chips |")
                                
                            if len(set(line3)) == 1:
                                profit += slot_multi[str(line3[0])] * int(message.content.split()[2])
                                wins.append(" 3x " + str(line3[0]) + " - "  + str(slot_multi[str(line3[0])] * int(message.content.split()[2])) + " Chips |")
                                
                            elif len(set(sline3)) == 1:
                                profit += slot_multi2[str(line3[0])] * int(message.content.split()[2])
                                wins.append(" 2x " + str(line3[0]) + " - "  + str(slot_multi2[str(line3[0])] * int(message.content.split()[2])) + " Chips |")
                            
                            elif p11 == "7" or p21 == "7" or p31 == "7":
                                profit += 3 * int(message.content.split()[2])
                                if int(message.content.split()[1]) == 3:
                                    wins.append(" 1x 7 - " + str(4 * int(message.content.split()[2])) + " Chips |")
                                    
                            if int(message.content.split()[1]) > 3:
                                line4 = [p11, p22, p33]
                                line5 = [p31, p22, p13]
                                sline4 = [p11, p22]
                                sline5 = [p31, p22]   
                                
                                if len(set(line4)) == 1:
                                    profit += slot_multi[str(line4[0])] * int(message.content.split()[2])
                                    wins.append(" 3x " + str(line4[0]) + " - "  + str(slot_multi[str(line4[0])] * int(message.content.split()[2])) + " Chips |")
                    
                                elif len(set(sline4)) == 1:
                                    profit += slot_multi2[str(line4[0])] * int(message.content.split()[2])
                                    wins.append(" 2x " + str(line4[0]) + " - "  + str(slot_multi2[str(line4[0])] * int(message.content.split()[2])) + " Chips |")
                                    
                                if len(set(line5)) == 1:
                                    profit += slot_multi[str(line5[0])] * int(message.content.split()[2])
                                    wins.append(" 3x " + str(line5[0]) + " - "  + str(slot_multi[str(line5[0])] * int(message.content.split()[2])) + " Chips |")
                                    
                                elif len(set(sline5)) == 1:
                                    profit += slot_multi2[str(line5[0])] * int(message.content.split()[2])
                                    wins.append(" 2x " + str(line5[0]) + " - "  + str(slot_multi2[str(line5[0])] * int(message.content.split()[2])) + " Chips |")
                    
                                elif p11 == "7" or p21 == "7" or p31 == "7":
                                    profit += 2 * int(message.content.split()[2])
                                    if int(message.content.split()[1]) == 5:
                                        wins.append(" 1x 7 - " + str(6 * int(message.content.split()[2])) + " Chips |")
                    
                    slot_lay = [[p11, p12, p13], [p21, p22, p23], [p31, p32, p33]]
                    slot_lay = pd.DataFrame(slot_lay)
                    
                    string = ""
                    if wins != []:
                        string = "Win combinations:"
                        for i in wins:
                                string += i
                        string = string[:-1]   
                    await asyncio.sleep(2)
                    
                    print(profit)
                    print(total_betted)
                    print(profit - total_betted)
                    print("")
                    print(data_pd.iloc[index, 2])
                    
                    data_pd.iloc[index, 2] = data_pd.iloc[index, 2] + profit - total_betted
                    print("")
                    print(data_pd.iloc[index, 2])
                    
                    await channel.send("```fix\nPlayer: " + nome +"\n" + tabulate(slot_lay, headers=['1', '2', '3'],
                            tablefmt="fancy_grid") + "\n" + "You won: " + str(profit - total_betted) + " Chips in the slot!" + "\n" + string + "```" , delete_after = 30)
                    
                    false_calc()
                
            if message.content in statements_dict:
                await channel.send(statements_dict[message.content], delete_after = 60)
            elif message.content == "$mychips":
                nome = data_pd.loc[data_pd['Discord ID'] == str(user_id), "Name"].iloc[0]
                await channel.send(nome + "'s current Chip Count is: " + str(chip_count(user_id)), delete_after = 15)
            
            elif message.content == "$rank":
                
                x = 1
                sorted_data = data_pd.sort_values(by=['Chips'], ascending = False)
                
                data_rank = []
                
                for account in range(0, len(data_pd)):
                    data_rank.append([str(x), sorted_data.iloc[account, 1], \
                         str(sorted_data.iloc[account, 2]), str(sorted_data.iloc[account, 3])])   
                    x += 1
    
                await channel.send("```fix\n Leaderboard\n" + tabulate(data_rank, headers=['Place', 'Name', 'Chips','#$rbet', '#$sbet'],
                                            tablefmt="fancy_grid") +"```" , delete_after = 60)


            elif message.content == "$quicksave":
                if user_id == 128967486434574336:
                    data_pd["Discord ID"] = data_pd["Discord ID"] + "a"
                    set_with_dataframe(sheet, data_pd)  

        await asyncio.sleep(5)
        await message.delete()
          
client.run("NzkwMjU3NDE4NzI5OTQ3MTc3.X99-kg.i8Dx6YiXZhLvD0MChwNgHqZ4fdw")
