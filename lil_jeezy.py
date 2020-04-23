#!/usr/bin/python3
import socket
import re
import random
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "chat.freenode.net" # Server
channel = "##programming" # Channel
botnick = "lil_jeezy" # Your bots nick

def joinchan(chan): # join channel(s).
    ircsock.send(bytes("JOIN "+ chan +"\n", "UTF-8")) 
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:  
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('nr')
        print(ircmsg)

def ping(): # respond to server Pings.
    return ircsock.send(bytes("PONG :pingisn", "UTF-8"))
     

def sendmsg(msg, target=channel): # sends messages to the target.
    return ircsock.send(bytes("PRIVMSG "+ target +" :"+ msg +"\n", "UTF-8"))

def jankify(text):
    text = list(text)
    for i in range(len(text)):
        if random.randint(0, 1) == 1:
            text[i] = text[i].upper()
        else:
            text[i] = text[i].lower()
            pass
    text = ''.join(text) 
    return text

def VERSE(verse, bible):
    mean_words = ['you Heathen', 'you Infidel', 'you Blasphemer', 'you Mongrel', 'you are the reason your mom died', 'lil_jeezy out', 'you NINCOMPOOP']
    try:
        return sendmsg(jankify(bible[verse]))
    except:
        return sendmsg("That isn't in THEBIBLE.TXT, {0}".format(random.choice(mean_words))) #won't be executed unless BLESS_USERis not being used the way it is 

def BLESS_USER(u_name):
    blessings = ['Spranklez of Mountain Dew all over {0}', "By Ozzy Osbourne's Bat, {0} is BLESSED", "BE BLESSED {0}", "The Holy Order of Mechanical Keybords ordains {0} as a High Priest of Clacky-ness", ".BlEsS", "Rise Child, for you are Blessed {0}", "lil_jeezy died for {0}'s sins", "https://www.youtube.com/watch?v=DLzxrzFCyOs", "emacs has a jesus mode ya know"]
    
    return sendmsg(random.choice(blessings).format(u_name))
    


def main():
    bible = {}
   
    f = open('THEBIBLE.TXT', 'r') 
    for i in range(93307):
        verse = f.readline()
        text = f.readline()
        verse = re.sub('[\n\r]', '', verse)
        text = re.sub('[\n\r]', '', text)
        f.readline()
        
        bible[verse.lower()] = text
    
    ircsock.connect((server, 6667)) # Here we connect to the server using the port 6667
    ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n", "UTF-8")) #We are basically filling out a form with this line and saying to set all the fields to the bot nickname.
    ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8")) # assign the nick to the bot

    joinchan(channel)
    
    while 1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('nr') 
        print(ircmsg)
        
        if ircmsg.find("PRIVMSG") != -1:
            name = ircmsg.split('!',1)[0][1:]
            message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
            message = re.sub('[\n\r]', '', message)
            
            if message[:6] == '.verse':
                VERSE(message[7:].lower(), bible)    
            
            if message[:6] == '.bless': 
                BLESS_USER(message[7:])
        
        elif ircmsg.find("PING :") != -1:
            ping()

if __name__ == "__main__":
    main()
