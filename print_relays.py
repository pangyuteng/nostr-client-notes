import json
import sys
import requests

def save_to_json():
    with open('out.txt','r') as f:
        c = [x for x in f.read().split('\n') if len(x) > 0]
    mylist = []
    for x in c:
        myitem = x.replace(": rw","")
        mylist.append(myitem)
    with open('relays.json','w') as f:
        f.write(json.dumps(mylist,sort_keys=True,indent=4))


def delete_relay():
    with open('out.txt','r') as f:
        c = [x for x in f.read().split('\n') if len(x) > 0]

    for x in c:
        my = "./noscl relay remove "+x.replace(": rw","")
        print(my)

def add_relay():
    json_file = sys.argv[1]
    with open(json_file,'r') as f:
        c = json.loads(f.read())

    for uri in c['relays']:
        url = uri.replace("wss://","https://")
        try:
            r = requests.get(url, timeout=2) 
            print(f"{r.status_code} \t{url}")
        except:
            print(f"timeout. \t{url}")
            continue
        response_str = r.content.decode('utf-8')
        if response_str == "Please use a Nostr client to connect.":
            a = f'./noscl relay add {uri}\n'
            with open('batch-add.sh','a+') as f:
                f.write(a)
            b = f'./noscl relay remove {uri}\n'
            with open('batch-remove.sh','a+') as f:
                f.write(b)
    
if __name__ == "__main__":
    pass
    save_to_json()
