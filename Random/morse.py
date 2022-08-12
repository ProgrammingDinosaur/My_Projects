import json

def DecodeMorse(message: str):
    decoded_message = ""
    with open("morse_data.json","r") as morsefile:
       chains = morsefile.read()
       data = json.loads(chains)
       for letter in message:
        if letter == " ":
            decoded_message+= " "
        else:
            decoded_message += (data[letter.lower()]+" ")
    print(decoded_message)


message = input("Please enter your message to translate to morse: ")
DecodeMorse(message)