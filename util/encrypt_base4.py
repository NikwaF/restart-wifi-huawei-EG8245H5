import base64 

def base64_to_string(word: str) -> None : 
    convert = base64.b64encode(str.encode(word))
    return convert.decode('utf-8')