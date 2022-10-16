import re 
import os
import shutil

# TODO: Implement more exeptions where needed, optimize code, and add gpg search support (whenever i feel like it).

"""
NOTE: This asumes you are using a linux distribution with opengpg and basic packages installed.

This class helps traslate text into the international morse code standard
You need:
receiber: Some gpg public key's associated email as the morse output will be signed and encrypted. 
filename: the name of the output file
path: the path of the output file
sentence (optional): You can traslate a sentence or an entire file into the international morse code standard
output file (optional): You can input a whole file
"""

class Morse:
    def __init__(self,receiber = None,filename = "output.txt",path = "output",sentence = None, inputFile = None):
        self.sentence = sentence
        self.inputFile = inputFile
        self.cleanedInputFile = None
        self.traduced = None
        self.filename = filename
        self.path = path
        self.receiber = receiber
        self.traducer = {
            "a":".-",
            "b":"-...",
            "c":"-.-.",
            "d":"-..",
            "e":".",
            "f":"..-.",
            "g":"--.",
            "h":"....",
            "i":"..",
            "j":".---",
            "k":"-.-",
            "l":".-..",
            "m":"--",
            "n":"-.",
            "o":"---",
            "p":".--.",
            "q":"--.-",
            "r":".-.",
            "s":"...",
            "t":"-",
            "u":"..-",
            "v":"...-",
            "w":".--",
            "x":"-..-",
            "y":"-.--",
            "z":"--..",
            "0":"------",
            "1":".----",
            "2":"..---",
            "3":"...--",
            "4":"....-",
            "5":".....",
            "6":"-....",
            "7":"--...",
            "8":"---..",
            "9":"----.",
            ".":".-.-.-",
            ",":"--..--",
            "?":"..--..",
            "\n":"\n"
        }

        if self.sentence is None and self.inputFile is None:
            raise NO_PLAIN_TEXT_INPUT_ERROR("Neither plain text string nor input file was provided")
    
        elif self.sentence is not None:
            self.sentence =  self.cleanSentence(self.sentence)

        else:
            if ".txt" not in self.inputFile:
                error = f"The input file {self.inputFile} is not a textfile."
                raise NO_TEXT_FILE_EXEPTION(error)
            else:
                # new filename for saving a text-clean version
                self.cleanedInputFile = self.inputFile[0:-4] + "_cleaned" + ".txt"
                self.cleanFile()

    # convert an entire file to lower case and remove unsupported characters
    def cleanFile(self):
        # check if the file exist. Otherwise, launch exeption
        if os.path.exists(self.inputFile) and os.path.isfile(self.inputFile):
            # first open the file in read mode to extract "corrupted files"
            sentences = self.readFileLines(self.inputFile)
            # open the file in write mode to write the exorcised sentences into it
            fileOpen = open(self.cleanedInputFile,"w")
            for sentence in sentences:
                sentence = self.cleanSentence(sentence)
                fileOpen.write(sentence)
            fileOpen.close()
        
        else:
            error = f"File {self.inputFile} does not exist"
            raise INPUT_FILE_NOT_FOUND_ERROR(error)

    # convert to lower case and remove unspported characters in morse 
    def cleanSentence(self,sentence):
        cleaned = sentence.lower()
        cleaned = re.sub("[-'!¡¿+/*\"\'{(#)}%&=~:;|]{1,}","",cleaned)
        return cleaned 

    # convert a sentence to morse code
    def traduce(self,sentence):
        res = ""
        for ch in sentence:
            if ch == " ":
                res += ch
            else:
                res += self.traducer[ch]
        return res
    
    # leaves the output directory clean and ready for writing the morse output file
    def createOutputDir(self):
        if os.path.exists(self.path):
            shutil.rmtree(self.path)
        os.mkdir(self.path)
        os.chdir(self.path)

    # reads the lines from a file and returns them in a list of strings
    def readFileLines(self,file):
        fileOpen = open(file,"r")
        sentences = fileOpen.readlines()
        fileOpen.close()
        return sentences

    # export the input sentence into a text file with morse code
    def exportFileFromSentence(self,prepare = True):
        self.traduced = self.traduce(self.sentence)
        self.createOutputDir()
        textFile = open(self.filename,"w")
        textFile.write(self.traduced)
        textFile.close()
        if prepare:
            self.zipEncrypt()

    # export the cleaned input text file into a file with morse code 
    def exportFileFromTextFile(self,prepare = True):
        # TODO: traduce the cleaned text file into morse and export it in a similar way as the function above
        # read the clean lines
        sentences = self.readFileLines(self.cleanedInputFile)
        # change into the output directory
        self.createOutputDir()      
        # process and white the morse code lines into the output filename
        textFile = open(self.filename,"w")
        for sentence in sentences:
            traduced = self.traduce(sentence)
            textFile.write(traduced)
        textFile.close()
        if prepare:
            self.zipEncrypt()

    # optional: sign and encrypt the output file. Requires al least one receiber
    def zipEncrypt(self):
        if self.receiber is None:
            raise NO_RECEIBER_FOUND_EXCEPTION("No GPG receiber was entered into the constructor")
        # asumes the system is in the output file already
        command = f"gpg --encrypt --sign --armor -r {self.receiber} {self.filename}"
        os.system(command)
        os.remove(self.filename)
        os.chdir("..")
        os.system(f"zip -r {self.path}.ziṕ {self.path}")

# custom exepctions

class NO_PLAIN_TEXT_INPUT_ERROR(Exception):
    # raise if no input file is supplied
    pass

class INPUT_FILE_NOT_FOUND_ERROR(Exception):
    # raise if the file is not found in the system
    pass

class NO_TEXT_FILE_EXEPTION(Exception):
    # raise if the file is not a text file 
    pass

class NO_RECEIBER_FOUND_EXCEPTION(Exception):
    # raise if no receiber was receibed or not found in GPG
    pass


