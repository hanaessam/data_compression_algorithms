
print("LZW Compression Algorithm")
print("=================================================================")
h = int(input("Enter 1 if you want to enter input in command window, 2 if you are using some file:"))
if h == 1:
    stringToEncode = input("Enter the string you want to compress:")
elif h == 2:
    file = input("Enter the filename:")
    with open(file, 'r') as f:
        stringToEncode = f.read()
else:
    print("You entered invalid input")

DefultDic = dict()
i = 0
while i < 128:
    DefultDic[chr(i)] = i
    i = i + 1


def encode_lzw(text):
    dictionary = DefultDic
    index = 128
    i = 0
    encoded = []
    while i < len(text):
        j = 0
        stringToBeSaved = text[i]

        while stringToBeSaved in dictionary and i + j < len(text):
            indexInDictionary = dictionary[stringToBeSaved]
            length = len(stringToBeSaved)
            if (i + j == len(text) - 1):
                break
            j = j + 1
            stringToBeSaved = stringToBeSaved + text[i + j]
        i = i + length
        encoded.append(indexInDictionary)
        if (stringToBeSaved not in dictionary):
            dictionary[stringToBeSaved] = index
        index = index + 1

    return encoded, dictionary


l = []


def decode_lzw(encoded, dictionary):
    i = 0
    while i < len(encoded):
        if (encoded[i] < len(dictionary)):
            l.append(list(dictionary.keys())[list(dictionary.values()).index(encoded[i])])
        else:
            tmp = dictionary[encoded[i - 1]]
            tmp += tmp[0]
            dictionary[tmp] = encoded[i]
            l.append(list(dictionary.keys())[list(dictionary.values()).index(encoded[i])])
        i = i + 1

print("Enetered string is:", stringToEncode)
[encoded, dictionary] = encode_lzw(stringToEncode)
a = encoded
print(encoded)

output = open("compressed.txt", "w+")
output.write(str(a))
print("Compressed file generated as compressed.txt")
output = open("compressed.txt", "w+")
decode_lzw(encoded, DefultDic)
print("Decoded string:", "".join(l))