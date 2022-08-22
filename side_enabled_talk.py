import time
import json
import os
from gtts import gTTS
from mutagen.mp3 import MP3

class foreColor:
    ERROR = '\x1b[1;33;41m'
    WARNING = '\x1b[1;30;43m'
    VERIFICATION = '\x1b[6;30;44m'
    PASSED = '\x1b[6;30;42m'
    END = '\033[0m'

while True:
    try:
                

        #Dosyadan verileri al

        waiting_for_talking = open("data/waiting_for_talking.txt", "r", encoding="utf-8")
        waiting_for_talking_read = waiting_for_talking.readlines()
        waiting_for_talking.close()

        #Dosyayi Temizle

        delete_talking_words = open("data/waiting_for_talking.txt", "w", encoding="utf-8")
        delete_talking_words.write("")
        delete_talking_words.close()

        #Whitelist'i oku

        whitelist = open("data/whitelist.json", "r", encoding="utf-8")
        whitelist_list = json.loads(whitelist.read())
        whitelist.close()


        for word in waiting_for_talking_read:
            start = time.time()
            if "\n" in word:
                word = word.replace("\n", "")
            
            dtt = word.split(":")
            word = dtt[0]
            
            side = word.split("-")[0]
            substance = word.split("-")[1]
            file_name = substance
            if "_" in substance:    
                substance = substance.replace("_", " ")
                    
            print(foreColor.VERIFICATION + "--NORMALIZED--" + foreColor.END)
            print(foreColor.PASSED + " " +substance + " " + foreColor.END)

            if substance in whitelist_list:
                print(foreColor.PASSED + "PASSED WHITELIST" + foreColor.END)

                if side == "R":
                    read_text = "Sağınızda " + substance + " var." 
                else:
                    read_text = "Solunuzda " + substance + " var." 
                soundfile = gTTS(text=read_text, lang='tr')
                soundfile.save("sounds/" + file_name + ".mp3")
                length = MP3("sounds/" + file_name + ".mp3").info.length
                os.system("start sounds/" + file_name + ".mp3") # Raspberry --> start -> aplay
                time.sleep(length + 0.2)
            else:
                print(foreColor.ERROR + "ERROR! DATA NOT IN WHITELIST" + foreColor.END)

            end = time.time()
            print(end-start)
            print("\n")
                    
    except Exception as e:
        print(foreColor.ERROR + "We have a problem Houston" + foreColor.END)
