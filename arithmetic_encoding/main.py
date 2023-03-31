from decimal import Decimal
from tkinter import *
import sys
from collections import defaultdict


def binary_encode(probabilities, message):
    """Arithmetic binary encoding"""
    low = 0
    high = 1
    result = ""
    for symbol in message:
        range_ = high - low
        high = low + probabilities[symbol] * range_
        low = low + (probabilities[symbol - 1] if symbol > 0 else 0) * range_
    for i in range(64):
        if low >= 0.5:
            result += "1"
            low -= 0.5
        else:
            result += "0"
            low *= 2
        if high <= 0.5:
            result += "0"
            high *= 2
        else:
            result += "1"
            high = 2 * high - 1
    return result

def binary_decode(probabilities, message):
    """Arithmetic binary decoding"""
    low = 0
    high = 1
    code = int(message[:32], 2)
    value = int(message[32:], 2)
    result = []
    while True:
        range_ = high - low
        symbol = 0
        while probabilities[symbol] <= (value - low) * range_:
            symbol += 1
        result.append(symbol)
        high = low + probabilities[symbol] * range_
        low = low + (probabilities[symbol - 1] if symbol > 0 else 0) * range_
        if low > code / 2:
            value = (value - code // 2) * 2
            code = code // 2
        elif high < code / 2:
            value = value * 2 + 1
            code = code // 2
        else:
            break
    return result

def float_encode(probabilities, message):
    """Arithmetic floating point encoding"""
    low = 0.0
    high = 1.0
    result = ""
    for symbol in message:
        range_ = high - low
        high = low + probabilities[symbol] * range_
        low = low + (probabilities[symbol - 1] if symbol > 0 else 0) * range_
    while True:
        if high < 0.5:
            result += "0"
            high = 2 * high
            low = 2 * low
        elif low >= 0.5:
            result += "1"
            high = 2 * (high - 0.5)
            low = 2 * (low - 0.5)
        else:
            break
    result += "{0:b}".format(int(round((low + high) / 2 * 2**32)))
    return result

def float_decode(probabilities, message):
    """Arithmetic floating point decoding"""
    low = 0.0
    high = 1.0
    value = int(message[-32:], 2) / 2**32
    message = message[:-32]
    result = []
    while True:
        range_ = high - low
        symbol = 0
        while probabilities[symbol] <= (value - low) * range_:
            symbol += 1
        result.append(symbol)
        high = low + probabilities[symbol] * range_
        low = low + (probabilities[symbol - 1] if symbol > 0 else 0) * range_
        if high < 0.5:
            high = 2 * high
            low = 2 * low
            value = 2 * value
        elif low >= 0.5:
            high = 2 * (high - 0.5)
            low = 2 * (low - 0.5)
            value = 2 * (value - 0.5)
        else:
            break
    return result


def compress_string(string, encoding_func):
    """Compresses a string using the specified encoding function"""
    counts = defaultdict(int)
    for char in string:
        counts[char] += 1
    probabilities = [counts[char] / len(string) for char in range(256)]
    encoded = encoding_func(probabilities, [ord(char) for char in string])
    return encoded

def decompress_string(string, decoding_func):
    """Decompresses a string using the specified decoding function"""
    counts = defaultdict(int)
    for char in string:
        counts[char] += 1
    probabilities = [counts[char] / len(string) for char in range(256)]
    decoded = decoding_func(probabilities, string)
    return "".join([chr(char) for char in decoded])

def compress_file(input_file, output_file, encoding_func):
    """Compresses a file using the specified encoding function"""
    with open(input_file, "rb") as f:
        data = f.read()
    encoded = compress_string(data.decode("latin1"), encoding_func)
    with open(output_file, "wb") as f:
        f.write(encoded.encode("utf8"))

def decompress_file(input_file, output_file, decoding_func):
    """Decompresses a file using the specified decoding function"""
    with open(input_file, "rb") as f:
        data = f.read().decode("utf8")
    decoded = decompress_string(data, decoding_func)
    with open(output_file, "wb") as f:
        f.write(decoded.encode("latin1"))


print("Arithmetic Encoding Program")
print("===========================")
choice = int(input("Enter 1 if you want to enter in command window, 2 if you are using some file:"))
if choice == 1:
    original_msg = input("Enter the string you want to compress:")
    print("You entered:", original_msg)
    print("Enter 1 if you want to use binary encoding, 2 if you want to use floating point encoding:")
    choice = int(input("Enter your choice:"))
    if choice == 1:
        print("You entered binary encoding")
        print("The compressed string is:", compress_string(original_msg, binary_encode))
        print("The decompressed string is:", decompress_string(compress_string(original_msg, binary_encode), binary_decode))
    elif choice == 2:
        print("You entered floating point encoding")
        print("The compressed string is:", compress_string(original_msg, float_encode))
        print("The decompressed string is:", decompress_string(compress_string(original_msg, float_encode), float_decode))
    else:
        print("You entered invalid input")
elif choice == 2:
    file = input("Enter the filename:")
    print("Enter 1 if you want to use binary encoding, 2 if you want to use floating point encoding:")
    choice = int(input("Enter your choice:"))
    if choice == 1:
        print("You entered binary encoding")
        with open(file, 'r') as f:
            original_msg = f.read()
            compress_file(file, "compressed.bin", binary_encode)
            decompress_file("compressed.bin", "decompressed.txt", binary_decode)
    elif choice == 2:
        print("You entered floating point encoding")
        with open(file, 'r') as f:
            original_msg = f.read()
            compress_file(file, "compressed.bin", float_encode)
            decompress_file("compressed.bin", "decompressed.txt", float_decode)
else:
    print("You entered invalid input")

uncompressed_file_size = len(original_msg)*8
compressed_file_size = len(compress_file(file, "compressed.bin", float_encode))-2
print("Your original file size was", uncompressed_file_size,"bits. The compressed size is:",compressed_file_size)
output = open("compressed.txt","w+")
print("Compressed file generated as compressed.txt")
output = open("compressed.txt","w+")
output.write(compress_file(file, "compressed.bin", float_encode))


