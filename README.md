# morse_traduction
Convert text files or sentences to the international morse code and export them to text files with the option to sign and encrypt them. 


# Documentation:
## Requierements:
- gnupg in a linux distribution
- zip package in a linux distribution
- python 3
- You need our own GPG Key and to import someone's public key

*It uses gnupg terminal commands.*


### Sample program (From text file):
```
from morse_traducer import Morse

def main():
    f = "example.txt"
    r = "some_mail@gmail.com"
    m = Morse(inputFile=f,receiber = r)
    m.exportFileFromTextFile(prepare=True)

if __name__ == "__main__":
    main()
```

### Sample program (From sentence):
```
from morse_traducer import Morse

def main():
    s = "some stuff"
    r = "some_mail@gmail.com"
    m = Morse(sentence = s,receiber = r)
    m.exportFileFromSentence(prepare=True)

if __name__ == "__main__":
    main()

```
*Use ```prepare = False ``` if you do not wish to sign and encrypt the output file using the receiver's public key.*


### More detailed explanaition comming soon...
