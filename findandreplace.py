from os import listdir
from os.path import isfile, join, dirname, abspath
import sys

target = input("Replace ")
replacement = input("with ")

left_allowed_characters = ["'", " ", "\"", ",",""] #To avoid messing with internal variables, only occurrences with these characters on its sides will be replaced
right_allowed_characters = ["'", " ", "\"", ",", "."]
extension = ".int" #Only files with this extension will be checked

#Do no touch these at all
typeAfiles = ["DishonoredEditor", "GFxUI"]
typeAfiles = [file+extension for file in typeAfiles] #add extension

#Files with the format something=something
typeBfiles = ["Scoring", "RPG", "Settings"]
typeBfiles = [file+extension for file in typeBfiles]



#Directory where the script is
if getattr(sys, 'frozen', False):
    directory = dirname(sys.executable) #directory when using .exe
else:
    directory = dirname(abspath(__file__)) #directory when using .py

#List with all the files in directory finishing in extension
files = [file for file in listdir(directory) if file[-4:].lower() == extension and isfile(join(directory, file))]

file_counter = 1;
with open("log.txt", 'w') as log:
    for file in files:
        if file in typeAfiles:
            n_swaps = 0
            n_occurences = 'X'
            continue
        if file in typeBfiles:
            f = open(file, encoding = "utf-16")
            text = f.readlines()
            f.close()

            n_occurrences = 0
            n_swaps = 0
            swapped_text=[]
            for line in text:
                if '=' not in line: #this line shouldn't be changed
                    swapped_text.append(line)
                    continue

                split_line = line.split('=')
                reader = split_line[1].find(target) #we only look at the right side of the '='
                if reader == -1: #No occurrence
                    swapped_text.append(line)
                    continue

                if(target in split_line[0]):
                    n_occurrences += 2
                    n_swaps += 1
                else:
                    n_occurrences += 1
                    n_swaps += 1

                split_line[1] = split_line[1].replace(target, replacement) #target is swapped with replacement
                log.write("In " + file + ": " + line + "\n")
                swapped_text.append('='.join(split_line))

            if n_swaps:
                f = open(file, 'w', encoding = "utf-16")
                f.writelines(swapped_text)
                f.close()
        else:
            try:
                with open(file, encoding = "utf-16") as f: #I don't know why but some files don't work otherwise
                    text = f.read()
                    encoding = "utf-16"
            except:
                with open(file) as f:
                    text = f.read()
                    encoding = None

            reader = text.find(target) #index of the first occurence (-1 if there's none)

            n_occurrences = 0;
            n_swaps = 0
            while reader != -1:
                n_occurrences += 1
                left_char = text[reader-1]
                right_char = text[reader + len(target)]
                if left_char in left_allowed_characters and right_char in right_allowed_characters: #The sides of the substring are allowed characters
                    log.write("In " + file + ": ..." + text[reader-10:reader+len(target)+10].replace('\n',' ') + "..." + "\n")
                    n_swaps+=1
                    text = text[:reader] + replacement + text[reader+len(target):]

                reader = text.find(target, reader + min(len(target), len(replacement))) #finds the index of the next occurence

            if n_swaps:
                f = open(file, 'w', encoding = encoding)
                f.write(text)
                f.close()



        if n_swaps:
            print('\033[94m'+f"[{file_counter:03}/{len(files)}] {n_swaps}/{n_occurrences} occurences swapped in {file}")
        elif n_occurrences:
            print('\033[96m'+f"[{file_counter:03}/{len(files)}] {n_swaps}/{n_occurrences} occurences swapped in {file}")
        else:
            print('\033[0m'+f"[{file_counter:03}/{len(files)}] {n_swaps}/{n_occurrences} occurences swapped in {file}")
        file_counter += 1

input()
