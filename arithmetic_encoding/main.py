from decimal import Decimal
from tkinter import *

print("Arithmetic Encoding Program")
print("===========================")
choice = int(input("Enter 1 if you want to enter in command window, 2 if you are using some file:"))
if choice == 1:
    original_msg = input("Enter the string you want to compress:")
elif choice == 2:
    file = input("Enter the filename:")
    with open(file, 'r') as f:
        original_msg = f.read()
else:
    print("You entered invalid input")
len_my_string = len(original_msg)
print ("Enetered string is:", original_msg)

frequency_table = {}

for i in original_msg:
    if i in frequency_table:
        frequency_table[i] += 1
    else:
        frequency_table[i] = 1

print("Original Message: {msg}".format(msg=original_msg))


def get_probability_table(frequency_table):
    """
    Calculates the probability table out of the frequency table.
    """
    total_frequency = sum(list(frequency_table.values()))

    probability_table = {}
    for key, value in frequency_table.items():
        probability_table[key] = value / total_frequency

    return probability_table

"""
save_stages: If True, then the intervals of each stage are saved in a list. 
"""
save_stages = True
probability_table = get_probability_table(frequency_table)


def get_encoded_value(last_stage_probs):
    """
    After encoding the entire message, this method returns the single value that represents the entire message.
    last_stage_probs: A list of the probabilities in the last stage.

    Returns the minimum and maximum probabilites in the last stage in addition to the value encoding the message.
    """
    last_stage_probs = list(last_stage_probs.values())
    last_stage_values = []
    for sublist in last_stage_probs:
        for element in sublist:
            last_stage_values.append(element)

    last_stage_min = min(last_stage_values)
    last_stage_max = max(last_stage_values)
    encoded_value = (last_stage_min + last_stage_max) / 2

    return last_stage_min, last_stage_max, encoded_value

def process_stage(probability_table, stage_min, stage_max):
        """
        Processing a stage in the encoding/decoding process.
        probability_table: The probability table.
        stage_min: The minumim probability of the current stage.
        stage_max: The maximum probability of the current stage.

        Returns the probabilities in the stage.
        """

        stage_probs = {}
        stage_domain = stage_max - stage_min
        for term_idx in range(len(probability_table.items())):
            term = list(probability_table.keys())[term_idx]
            term_prob = Decimal(probability_table[term])
            cum_prob = term_prob * stage_domain + stage_min
            stage_probs[term] = [stage_min, cum_prob]
            stage_min = cum_prob

        return stage_probs


def encode(msg, probability_table):
        """
        Encodes a message using arithmetic encoding.
        msg: The message to be encoded.
        Returns the encoder, the floating-point value representing the encoded message
        & the maximum and minimum values of the interval in which the floating-point value falls.
        """

        msg = list(msg)
        encoder = []
        stage_min = Decimal(0.0)
        stage_max = Decimal(1.0)

        for msg_term_idx in range(len(msg)):
            stage_probs = process_stage(probability_table, stage_min, stage_max)

            msg_term = msg[msg_term_idx]
            stage_min = stage_probs[msg_term][0]
            stage_max = stage_probs[msg_term][1]

            if save_stages:
                encoder.append(stage_probs)

        last_stage_probs = process_stage(probability_table, stage_min, stage_max)

        if save_stages:
            encoder.append(last_stage_probs)

        interval_min_value, interval_max_value, encoded_msg = get_encoded_value(last_stage_probs)

        return encoded_msg, encoder, interval_min_value, interval_max_value

# Encode the message
print("Frequency Table: ", frequency_table)
print("Probability Table: ", probability_table)
encoded_msg, encoder , interval_min_value, interval_max_value = encode(msg=original_msg, probability_table=probability_table)
print("Encoded Message: {msg}".format(msg=encoded_msg))


def process_stage_binary(float_interval_min, float_interval_max, stage_min_bin, stage_max_bin):
    """
    Processing a stage in the encoding/decoding process.
    float_interval_min: The minimum floating-point value in the interval.
    float_interval_max: The maximum floating-point value in the interval.
    stage_min_bin: The minimum binary number in the current stage.
    stage_max_bin: The maximum binary number in the current stage.
    Returns the probabilities of the terms in this stage. There are only 2 terms.
    """

    stage_mid_bin = stage_min_bin + "1"
    stage_min_bin = stage_min_bin + "0"

    stage_probs = {}
    stage_probs[0] = [stage_min_bin, stage_mid_bin]
    stage_probs[1] = [stage_mid_bin, stage_max_bin]

    return stage_probs


def float2bin(float_num, num_bits=None):
    """
    Converts a floating-point number into binary.
    float_num: The floating-point number.
    num_bits: The number of bits expected in the result. If None, then the number of bits depends on the number.
    Returns the binary representation of the number.
    """

    float_num = str(float_num)
    if float_num.find(".") == -1:
        # No decimals in the floating-point number.
        integers = float_num
        decimals = ""
    else:
        integers, decimals = float_num.split(".")
    decimals = "0." + decimals
    decimals = Decimal(decimals)
    integers = int(integers)

    result = ""
    num_used_bits = 0
    while True:
        mul = decimals * 2
        int_part = int(mul)
        result = result + str(int_part)
        num_used_bits = num_used_bits + 1

        decimals = mul - int(mul)
        if type(num_bits) is type(None):
            if decimals == 0:
                break
        elif num_used_bits >= num_bits:
            break
    if type(num_bits) is type(None):
        pass
    elif len(result) < num_bits:
        num_remaining_bits = num_bits - len(result)
        result = result + "0" * num_remaining_bits

    integers_bin = bin(integers)[2:]
    result = str(integers_bin) + "." + str(result)
    return result


def bin2float(bin_num):
    """
    Converts a binary number to a floating-point number.
    bin_num: The binary number as a string.
    Returns the floating-point representation.
    """
    if bin_num.find(".") == -1:
        # No decimals in the binary number.
        integers = bin_num
        decimals = ""
    else:
        integers, decimals = bin_num.split(".")
    result = Decimal(0.0)

    # Working with integers.
    for idx, bit in enumerate(integers):
        if bit == "0":
            continue
        mul = 2 ** idx
        result = result + Decimal(mul)

    # Working with decimals.
    for idx, bit in enumerate(decimals):
        if bit == "0":
            continue
        mul = Decimal(1.0) / Decimal((2 ** (idx + 1)))
        result = result + mul
    return result

def encode_binary(float_interval_min, float_interval_max):
        """
        Calculates the binary code that represents the floating-point value that encodes the message.
        float_interval_min: The minimum floating-point value in the interval.
        float_interval_max: The maximum floating-point value in the interval.
        Returns the binary code representing the encoded message.
        """

        binary_encoder = []
        binary_code = None

        stage_min_bin = "0.0"
        stage_max_bin = "1.0"

        stage_probs = {}
        stage_probs[0] = [stage_min_bin, "0.1"]
        stage_probs[1] = ["0.1", stage_max_bin]

        while True:
            if float_interval_max < bin2float(stage_probs[0][1]):
                stage_min_bin = stage_probs[0][0]
                stage_max_bin = stage_probs[0][1]
            else:
                stage_min_bin = stage_probs[1][0]
                stage_max_bin = stage_probs[1][1]

            if save_stages:
                binary_encoder.append(stage_probs)

            stage_probs = process_stage_binary(float_interval_min,float_interval_max,stage_min_bin,stage_max_bin)

            if (bin2float(stage_probs[0][0]) >= float_interval_min) and (
                    bin2float(stage_probs[0][1]) < float_interval_max):
                binary_code = stage_probs[0][0]
                break
            elif (bin2float(stage_probs[1][0]) >= float_interval_min) and (
                    bin2float(stage_probs[1][1]) < float_interval_max):
                binary_code = stage_probs[1][0]
                break

        if save_stages:
            binary_encoder.append(stage_probs)

        return binary_code, binary_encoder


# Get the binary code out of the floating-point value
binary_code, encoder_binary = encode_binary(float_interval_min=interval_min_value, float_interval_max=interval_max_value)
print("The binary code is: {binary_code}".format(binary_code=binary_code))


def decode(encoded_msg, msg_length, probability_table):
    """
    Decodes a message from a floating-point number.

    encoded_msg: The floating-point value that encodes the message.
    msg_length: Length of the message.
    probability_table: The probability table.
    Returns the decoded message.
    """

    decoder = []

    decoded_msg = []

    stage_min = Decimal(0.0)
    stage_max = Decimal(1.0)

    for idx in range(msg_length):
        stage_probs = process_stage(probability_table, stage_min, stage_max)

        for msg_term, value in stage_probs.items():
            if encoded_msg >= value[0] and encoded_msg <= value[1]:
                break

        decoded_msg.append(msg_term)

        stage_min = stage_probs[msg_term][0]
        stage_max = stage_probs[msg_term][1]

        if save_stages:
            decoder.append(stage_probs)

    if save_stages:
        last_stage_probs = process_stage(probability_table, stage_min, stage_max)
        decoder.append(last_stage_probs)

    return decoded_msg, decoder


# Decode the message
decoded_msg, decoder = decode(encoded_msg=encoded_msg, msg_length=len(original_msg), probability_table=probability_table)
decoded_msg = "".join(decoded_msg)
print("Decoded Message: {msg}".format(msg=decoded_msg))

print("Message Decoded Successfully? {result}".format(result=original_msg == decoded_msg))


uncompressed_file_size = len(original_msg)*8
compressed_file_size = len(binary_code)-2
print("Your original file size was", uncompressed_file_size,"bits. The compressed size is:",compressed_file_size)
output = open("compressed.txt","w+")
print("Compressed file generated as compressed.txt")
output = open("compressed.txt","w+")
output.write(binary_code)


"""
GUI part
"""
top = Tk()
top.title("Arithmetic Encoder")
top.minsize(300, 150)
enterLabel = Label(text="Enter the text you want to encode: ")
enterLabel.pack()
message = Entry()
message.pack()

def getGUI():
    original_msg =str(message.get())
    encoded_msg = encode(msg=original_msg,probability_table=probability_table)
    encodedLabel = Label(text=str(("The binary code is: {binary_code}".format(binary_code=binary_code))))
    encodedLabel.pack()
    orgSizeLabel = Label(text="Original Size = " + str(uncompressed_file_size))
    orgSizeLabel.pack()
    encodedSizeLabel = Label(text="Compressed Size = "+ str(compressed_file_size))
    encodedSizeLabel.pack()


btn = Button(text="Endode", command=getGUI)
btn.pack()

top.mainloop()