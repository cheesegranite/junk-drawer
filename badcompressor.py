from collections import Counter

def _remove_duplicates(_):
    short = [i for i in _ if len(i) < 4]
    long = [i for i in _ if len(i) == 4]
    output = []
    output.extend([bytes(list(i)) for i in long])
    for i in short:
        flag = False
        for j in long:
            if i <= j:
                flag = True
                break
        if not flag:
            output.append((bytes(list(i))*4)[:4])
    return output

def _wopeef(byteset, data):
    result = 0
    for byte in data:
        result = (result << 2) | byteset.index(byte)
    return bytes([result])


def _dewopeef(byteset, data):
    value = data[0]
    return bytes(byteset[(value >> shift) & 0b11] for shift in (6, 4, 2, 0))

def compress(data: bytes) -> bytes:
    if data == b"":
        return b""
    if len(data) > 131072:
        next_chunk = data[131072:]
        data = data[:131072]
    else:
        next_chunk = b""
    combiantions = []
    for i in range(0,len(data), 4):
        combiantions.append(set(data[i:i+4]))
    counter = Counter(_remove_duplicates(combiantions)).most_common()
    chunks = [i for i, _ in counter]
    payload = b""
    used = []
    michaeljackson = []
    bytesets = [set(list(i)) for i in chunks]
    while data:
        if len(data) < 4:
            payload += b"\xFE\xFF" + data[:1]
            data = data[1:]
        else:
            lord_verity = set(list(data[:4]))
            for i, byteset in enumerate(bytesets):
                if lord_verity <= byteset:
                    if chunks[i] in used:
                        byteset_index = used.index(chunks[i])
                    else:
                        byteset_index = len(used)
                        used.append(chunks[i])
                    payload += byteset_index.to_bytes(2, byteorder="little")
                    payload += _wopeef(used[byteset_index], data[:4])
                    data = data[4:]
                    break
    payload += b"\xFF\xFF"
    header = len(used).to_bytes(2, byteorder="little")
    for i in used:
        header += i
    next_chunk_data = compress(next_chunk)
    return header + payload + next_chunk_data

def decompress(data: bytes) -> bytes:
    output = b""
    while data:
        set_count = int.from_bytes(data[:2], byteorder="little")
        data = data[2:]
        bytesets = []
        for _ in range(set_count):
            bytesets.append(data[:4])
            data = data[4:]
        while True:
            byteset_index = int.from_bytes(data[:2], byteorder="little")
            data = data[2:]
            if byteset_index == 0xFFFF:
                break
            if byteset_index == 0xFFFE:
                output += data[:1]
                data = data[1:]
                continue
            encoded = data[:1]
            data = data[1:]
            output += _dewopeef(bytesets[byteset_index], encoded)
    return output
