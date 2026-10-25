import random

shuffled = lambda items: random.sample(items, len(items))

def choose_dict_name(bytebeat: str) -> str:
    letters = "abcdefghijklmnopqrstuvwxyz"
    numbers = "0123456789"
    names = shuffled([i for i in letters])
    while names:
        name = names.pop(0)
        if name not in bytebeat:
            return name
        names.extend(shuffled([name + i for i in letters+numbers]))

def find_special(bytebeat: str) -> list:
    ords = [ord(i) for i in bytebeat]
    special = [chr(i) for i in ords if not 0 <= i <= 255]
    return special

def obfuscate_num(number: str, prefix: str) -> str:
    normal = "0123456789"
    hexadecimal = "ABCDEF"
    if number in normal:
        n = int(number)
        return "(" + (prefix + "z(") * n + "''.length" + ")" * n + "+'')"
    elif number in hexadecimal:
        i = str(hexadecimal.index(number) + 1)
        return (f"{prefix}f({prefix}p("
                f"{prefix}s({obfuscate_num("4",prefix)})"
                f"+{prefix}s({obfuscate_num(i,prefix)})"
                f",{obfuscate_num("4",prefix)}**{obfuscate_num("2",prefix)}))")
    elif number == ",":
        return prefix + "c"
    else:
        raise ValueError("number isn't a hexadecimal number")

def filter_special(bytebeat: str) -> tuple:
    unique_special = set(find_special(bytebeat))
    filtered = ""
    special = []
    for i, char in enumerate(bytebeat):
        if char in unique_special:
            filtered += "X"
            special.append([i, char])
        else:
            filtered += char
    return filtered, special

def dict_encode(something: str) -> tuple:
    dictionary = []
    formatted_dict = []
    payload = []
    for char in something:
        if char not in dictionary:
            dictionary.append(char)
            formatted_dict.append(format(ord(char), "02X"))
    for char in something:
        payload.append(format(dictionary.index(char), "X"))
    return "".join(formatted_dict), ",".join(payload)

def mass_obfuscate_num(numbers: str, prefix: str) -> str:
    return "+".join([obfuscate_num(i, prefix) for i in numbers])

if 1:
    print("welcome to bytebeat obfuscator :3")
    print("note: dont obfuscate funcbeats")
    input_type = input("use file or paste bytebeat? (file/paste, leave blank for paste) >").strip().lower()[:1]
    if input_type == "f":
        bytebeat = input("enter file path >").removeprefix("\"").removesuffix("\"")
        encoding = input("enter file encoding (leave blank for utf-8) >").strip().lower()
        encoding = encoding if encoding else "utf-8"
        bytebeat = open(bytebeat, "r", encoding=encoding).read()
    elif input_type in ["p", ""]:
        bytebeat = input("enter bytebeat (one line) >")
    else:
        raise ValueError(f"input type \"{input_type}\" not supported")

    print("\n===== LOGS =====")
    var_prefix = choose_dict_name(bytebeat + "i")
    print("chosen variable prefix: " + var_prefix)
    unique = set([i for i in bytebeat])
    special = find_special(bytebeat)
    unique_special = set(special)
    print(f"bytebeat has:")
    print(f"{len(bytebeat)} characters")
    print(f"{len(unique)} unique characters")
    print(f"{len(special)} special characters")
    print(f"{len(unique_special)} unique special characters")

    obfuscated = ""
    obfuscated += f"/* made with cheesegranite's obfuscator */t?{var_prefix}n(t):(("
    obfuscated += var_prefix + "z=x=>x+1,"
    obfuscated += var_prefix + "p=parseInt,"
    obfuscated += var_prefix + "s=String,"
    obfuscated += var_prefix + "f=" + var_prefix + "s.fromCharCode,"
    obfuscated += var_prefix + "c=',',"
    print("header:\n" + obfuscated + "\n")

    filtered, special = filter_special(bytebeat)
    special = str(special).replace(" ", "")
    obfuscated += var_prefix + "e=" + special + ","

    lookup, payload = dict_encode(filtered)
    lookup = mass_obfuscate_num(lookup, var_prefix)
    payload = mass_obfuscate_num(payload, var_prefix)
    obfuscated += var_prefix + "a=" + lookup + ","
    obfuscated += var_prefix + "b=(" + payload + ").split(" + var_prefix + "c),"
    obfuscated += var_prefix + (f"d=Array.from({var_prefix}b,x=>{var_prefix}f({var_prefix}p({var_prefix}a[{var_prefix}p"
                                f"(x,({var_prefix}z({var_prefix}z({var_prefix}z({var_prefix}z(''.length))))+'')**("
                                f"{var_prefix}z({var_prefix}z(''.length))+''))*{var_prefix}z({var_prefix}z(''.length))]"
                                f"+{var_prefix}a[{var_prefix}p(x,({var_prefix}z({var_prefix}z({var_prefix}z("
                                f"{var_prefix}z(''.length))))+'')**({var_prefix}z({var_prefix}z(''.length))+''))*"
                                f"{var_prefix}z({var_prefix}z(''.length))+{var_prefix}z(''.length)],({var_prefix}z("
                                f"{var_prefix}z({var_prefix}z({var_prefix}z(''.length))))+'')**({var_prefix}z("
                                f"{var_prefix}z(''.length))+'')))),")
    obfuscated += var_prefix + "y=((s,f)=>{for(const[i,c]of s){f[i]=c;}return f;})" + (f"({var_prefix}e,{var_prefix}d)."
                                                                                       f"join(''),eval({var_prefix}y)),"
                                                                                       f"{var_prefix}n=eval('(t=>(\\n'+"
                                                                                       f"{var_prefix}y+'\\n))'),0)")
    with open("bytebeat_obfuscator.txt", "w", encoding="utf-8") as f:
        f.write(obfuscated)
    print("saved obfuscated bytebeat in bytebeat_obfuscator.txt\n\n===== END =====\nbytebeat obfuscated successfully")
