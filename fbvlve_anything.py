import base64
import ast
from collections import Counter

list_repr = lambda x: ",".join(str(i).removeprefix("0") for i in x)
huffman_tree = {
    "," : [0],
    "1" : [1,0,0,0],
    "2" : [1,0,0,1],
    "3" : [1,0,1,0],
    "4" : [1,0,1,1],
    "5" : [1,1,0,0],
    "6" : [1,1,0,1],
    "7" : [1,1,1,0,0],
    "8" : [1,1,1,0,1],
    "9" : [1,1,1,1,0],
    "0" : [1,1,1,1,1]
}

def convert_to_decimal(number):
    decimal = 0
    for bit in number:
        decimal *= 2
        decimal += int(bit)
    return decimal

def encode(data, error=1):
    encoded = []
    current = 0
    err0r = 0
    for i, sample in enumerate(data):
        if i % 1000 == 0:
            print(f"\rencoding... {i}/{len(data)}  {i/len(data):.1%} ", end="")
        err0r += abs(sample - current)
        if err0r > error:
            encoded.append(sample - current)
            current = sample
            err0r = 0
        else:
            encoded.append(0)
    print(f"\rencoding... {len(data)}/{len(data)} 100.0% ")

    print("finalizing...", end="")
    common = Counter(encoded).most_common()
    common_lookup = {value: i for i, (value, _) in enumerate(common)}
    common_fbvlve_lookup = [value for value, _ in common]
    encoded_fbvlve = [common_lookup[value] for value in encoded]

    huffman_ready = list_repr(encoded_fbvlve)

    encoded_bits = []
    for i, char in enumerate(huffman_ready):
        if i % 1000 == 0:
            print(f"\rfinalizing... {i}/{len(huffman_ready)}  {i/len(huffman_ready):.1%} ", end="")
        encoded_bits.extend(huffman_tree[char])

    bit_length = len(encoded_bits)

    while len(encoded_bits) % 8:
        encoded_bits.append(0)

    chunks = [encoded_bits[i:i + 8] for i in range(0, len(encoded_bits), 8)]

    chunks_new = []
    for chunk in chunks:
        chunk = "".join(str(bit) for bit in chunk)
        chunks_new.append(convert_to_decimal(chunk))
    chunks = bytes(chunks_new)
    print(f"\rfinalizing... {len(huffman_ready)}/{len(huffman_ready)} 100.0% ")
    return [common_fbvlve_lookup, base64.b64encode(chunks).decode("ascii"), bit_length]

TREE = {
    "0": ",",
    "1000": "1",
    "1001": "2",
    "1010": "3",
    "1011": "4",
    "1100": "5",
    "1101": "6",
    "11100": "7",
    "11101": "8",
    "11110": "9",
    "11111": "0"
}

def decode_huffman(data, bits):
    raw = base64.b64decode(data)
    decoded = ""
    code = ""
    for pos in range(bits):
        code += str((raw[pos >> 3] >> (7 - pos % 8)) & 1)
        if code in TREE:
            decoded += TREE[code]
            code = ""
    return decoded

def decode_fbvlve(data):
    values, bit_count, encoded = data
    indexes = [
        0 if x == "" else int(x)
        for x in decode_huffman(encoded, bit_count).split(",")
    ]
    a = 0
    output = []
    for i in indexes:
        a += values[i] if i < len(values) else 0
        output.append(a)
    return output

input_file = input("please enter file path:\n>")
eod = input("encode or decode fbvlve from file? (e/d):").lower().strip()[:1]

if eod == "e":
    compression = int(input("please enter compression level (lossy compression; will corrupt your files):\n>"))
    cooldata = list(open(input_file, "rb").read())
    encoded = encode(cooldata, error=compression)
    output = (
        "[[" +
        list_repr(encoded[0]) +
        "]," +
        str(encoded[2]) +
        ",`" +
        encoded[1] +
        "`]"
    )
    print(f"original: {len(cooldata)} bytes")
    print(f"encoded: {len(output)} bytes {"(lossy compressed)" if compression else ""}")
    print(f"compression ratio: {len(encoded)/len(cooldata):.1%}")
    with open("fbvlve.txt", "w", encoding="latin-1") as f:
        f.write(output)
elif eod == "d":
    with open(input_file, "r", encoding="latin-1") as f:
        data = ast.literal_eval(
            f.read()
            .replace("`", '"')
            .replace("[,", "[0,")
            .replace(",,", ",0,")
        )
    output = bytes(decode_fbvlve(data))
    with open("fbvlve.txt", "wb") as f:
        f.write(output)
else:
    raise ValueError("all i understood is ")
