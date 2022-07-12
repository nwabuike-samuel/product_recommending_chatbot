import requests
import tkinter
import ast

bot_name =  "Sami"

def ReadText(message):
    url = 'https://be24-194-59-249-251.eu.ngrok.io/webhooks/rest/webhook'
    myobj = {
        "message": message,
        "sender": "Samuel",
    }
    x = requests.post(url, json=myobj)
    ast.literal_eval(x.text)
    print(ast.literal_eval(x.text))
    # conversation.append("Innovate: "+"\n".join([ast.literal_eval(x.text)[0]["text"].split(" ")[3*(i-1):3*(i-1)+3] if len(ast.literal_eval(x.text)[0]["text"].split(" "))//10 >10 else ast.literal_eval(x.text)[0]["text"] for i in range(len(ast.literal_eval(x.text)[0]["text"].split(" "))//10)]))

    reply=""
    

    if len(ast.literal_eval(x.text)) > 1:
        for i in range(len(ast.literal_eval(x.text))):
            #print(ast.literal_eval(x.text)[i]["text"])
            #print("j now here")
            
            reply=""
            reply+=" ".join(ast.literal_eval(x.text)[i]["text"].split(" ")) + "\n"#[9 * (i - 1):9 * (i - 1) + 9]) + "\n"
            print(reply)
            return reply
    elif len(ast.literal_eval(x.text)[0]["text"].split(" ")) >50:
        for i in range(len(ast.literal_eval(x.text)[0]["text"].split(" "))//9 +1):
            reply+=" ".join(ast.literal_eval(x.text)[0]["text"].split(" ")[9 * (i - 1):9 * (i - 1) + 9]) + "\n"
            return reply
    else:
        reply=ast.literal_eval(x.text)[0]["text"]
        return reply
    #return reply

    # print([list(i.keys())[1] for i in ast.literal_eval(x.text)])
    # if 'image' in [list(i.keys())[1] for i in ast.literal_eval(x.text)]:
    #     def OpenImage():
    #         import webbrowser
    #         webbrowser.open(ast.literal_eval(x.text)[1]["image"].replace("\\",""))
    #     conversation.append("Innovate: " + ast.literal_eval(x.text)[1]["image"].replace("\\",""))
    #     b = tkinter.Button(root, text="Open Image",command=OpenImage).pack(...)
    # text.set("\n".join(conversation))