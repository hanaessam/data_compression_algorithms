print("LZ77 Compression Program")
print("=================================================================")
h = int(input("Enter 1 if you want to enter in command window, 2 if you are using some file:"))
if h == 1:
    my_string = input("Enter the string you want to compress:")
elif h == 2:
    file = input("Enter the filename:")
    with open(file, 'r') as f:
        my_string = f.read()
else:
    print("You entered invalid input")                    # taking user input
len_my_string = len(my_string)
print ("Enetered string is:",my_string)

encodedtuples = []


def sizes():
    choice = int(input("Press 1 if you want to enter search and lookahead size, Prses 2 to continue :"))
    if (choice == 2):
        sw = 100
        lh = 50
    elif (choice == 1):
        sw = int(input("Enter Search window size :"))
        lh = int(input("Enter lookahead window size :"))
    return sw, lh


maxSearchWindow, lookAheadWindow = sizes()


def encode():
    # Proccess data one char at a time (or skip chars if matches found)
    # Counts the number of chars already processed
    charCnt = 0

    while (charCnt < len(my_string)):
        '''Get a reference position, length of the longest match'''
        distance, length = getLongestMatch(charCnt)

        '''Find character of mismatch'''
        mismatchChar = my_string[charCnt + length]

        '''Append tuple'''
        encodedtuples.append((distance, length, mismatchChar))

        '''Shift the window (length + 1) positions along'''
        charCnt += (length + 1)


def getLongestMatch(charCnt):
    # Establish the size of the search window, because if we are at the beginning of the text we don't have as much characters in the search window as the length of the search window size
    searchWindowSize = min(charCnt, maxSearchWindow)

    # Establish the end of lookAheadWindow, because if we are at the end of the text then there aren't enaugh characters left to match the size of lookaheadwindow
    lookAheadWindowEnd = min(len(my_string) - charCnt, lookAheadWindow)

    # Search the buffer window for a match to the next character in the lookAhead window.
    distance = 0
    longestLength = 0

    for d in range(1, searchWindowSize + 1):
        # For all possible distances in searchWindow, try to find a new matchlength that is greater that the current longestLength
        length = 0

        while (my_string[charCnt - d + length] == my_string[charCnt + length] and length <= lookAheadWindowEnd):
            length += 1
            if (length > longestLength):
                longestLength = length
                distance = d
            elif (d < distance and length == longestLength):
                distance = d

    return distance, longestLength


def decode(tuples):
    reconstructedData = ''

    for distance, length, char in tuples:
        if (length == 0):
            # There was no match before this mismatch char, just concatenate it
            reconstructedData += char
        else:
            for _ in range(length):
                # length of reconstructedData is incremented by 1 each time we add a matched char, that is why distance doesn't need to change in statement below:
                currentChar = reconstructedData[len(reconstructedData) - distance]
                reconstructedData += currentChar
            reconstructedData += char
    return reconstructedData


encode()
for d, l, ch in encodedtuples:
    print('<' + str(d) + ',' + str(l) + ',' + ch + '> ')

print("Decoding the string :", decode(encodedtuples))


output = open("compressed.txt","w+")
print("Compressed file generated as compressed.txt")
output.write(str(encodedtuples))
output = open("compressed.txt","w+")

