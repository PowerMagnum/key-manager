from os import listdir, makedirs, getlogin
from os.path import isfile, join, basename, exists
from shutil import copyfile, move
from traceback import print_tb


user = getlogin()
base_path = "C:\\Users\\" + user + "\\.ssh\\"
mypath = base_path + "ssh-keys\\"
deleted_path = base_path + "deleted-keys\\"
used_file = "used.txt"


while True:
    command = input(">> ")
    match command.split():
        case ["exit"] | ["quit"] | [":q"]:
            break
        
        case ["help"] | ["key" , "-h"]:
            print("Mostra elenco chiavi: \t key show \t\t\t key -sh")
            print("Attiva una chiave: \t key set [key_name] \t\t key -s [key_name]")
            print("Aggiungi una chiave: \t key add [key_path] \t\t key -a [key_path]")
            print("Rimuovi una chiave: \t key remove [key_name] \t\t key -r [key_name]")
            print("Modifica una chiave: \t key edit [key_name] [new_name] \t key -e [key_name] [new_name]")
            print("Chiudi terminale: \t exit o quit")
            print("Autoconfigurazione: \t autoconfig")

        
        case ["key" , "show"] | ["key" , "-sh"]:
            files = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.find(".pub") == -1]
            with open(base_path + used_file, "r") as used:
                print("(Chiave attualmente in uso: " + used.read() + ")")
            for i in files:
                print(str(files.index(i))+")" , i)

        case ["key" , "edit", old_name, new_name] | ["key" , "-e", old_name, new_name]:
            move(mypath + old_name , mypath + new_name )
            with open(base_path + used_file, "r") as used:
                used_key = used.read()
            if used_key == old_name:
                with open(base_path + used_file, "w") as used:
                    used.write(new_name)
            print("Chiave aggiornata")
            

        case ["key" , "set" , key] | ["key" , "-s", key]: 
            files = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.find(".pub") == -1]
            if key in files:
                copyfile(mypath + key , base_path + "id_ed25519" )
                with open(base_path + used_file, "w") as used:
                    used.write(key)
                print("(Chiave attualmente in uso: " + key + ")")
            else:
                print("[Error]: Chiave non trovata")
        
        case ["key" , "add" , key_path] | ["key" , "-a", key_path]:
            file_name = basename(key_path).strip("\"")
            copyfile(key_path , mypath + file_name )
            print("Chiave aggiunta")

        case ["key" , "remove" , key] | ["key" , "-r", key]:
            move(mypath + key , deleted_path + key )
            print("Chiave rimossa (è possibile ripristinarla manualmente da .ssh)")

        case ["autoconfig"] | ["key", "-acfg"]:
            changes = False
            if not exists(mypath):
                makedirs(mypath)
                changes = True
            if not exists(deleted_path):
                makedirs(deleted_path)
                changes = True
            if not exists(base_path + used_file):
                with open(base_path + used_file, "w") as used:
                    used.write("None")
                changes = True
            if changes:
                print("Autoconfigurazione completata")
            else:
                print("Nessuna azione necessaria")

        case ["key", "set"] | ["key", "-s"]:
            print("Utilizzo: key set [key_name]")
        case ["key", "add"] | ["key", "-a"]:
            print("Utilizzo: key add [key_path]")
        case ["key", "remove"] | ["key", "-r"]:
            print("Utilizzo: key remove [key_name]")
        case ["key", "edit"] | ["key", "-e"]:
            print("Utilizzo: key edit [key_name] [new_name]")

        case _:
            print("Invalid command \"" + command + "\"")
            print("Digita \"help\" per informazioni")
    