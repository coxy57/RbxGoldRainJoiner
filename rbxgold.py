import json, websocket, time, re, requests, base64, random

# MADE BY COXY57 ON DISCORD
# MADE BY COXY57 ON DISCORD
# MADE BY COXY57 ON DISCORD
# MADE BY COXY57 ON DISCORD
# MADE BY COXY57 ON DISCORD
# MADE BY COXY57 ON DISCORD
# MADE BY COXY57 ON DISCORD
# MADE BY COXY57 ON DISCORD
# MADE BY COXY57 ON DISCORD

# This is made for rbxgold.com to join the rains automatically


x = "MADE BY coxy57 ON DISCORD"
y = "MADE BY coxy57 ON DISCORD"
z = "MADE BY coxy57 ON DISCORD"

# API KEY FOR CAPSOLVER.COM (you must create an account and get credit on the website then paste the key it gives you)
APIKEY = ""
# Your sid is your authentication for rbxgold.com
# To get it, go to the website https://rbxgold.com (you must be logged in and on pc)
# Press ctrl + shift + i
# Go to the application tab, if it doesnt show up click the >> on the top and it should show
# Click on cookies, then go to rbxgold.com, then copy the value next to the SID in the name column
# Paste it in between the "" in the SID =
SID = ""


class AutoJoinerHandler:
    def __init__(self, apikey):
        self.apikey = apikey
        self.website_key = "a3a5a9a9-7210-4dc7-a7bc-39c3fc73143e"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"

    def solve_captcha(self):
        if not all(v in globals() for v in ("x", "y", "z")): return False
        if self.apikey is None:
            return False
        captcha_created = requests.post('https://api.capsolver.com/createTask', json={
            "clientKey": self.apikey,
            "task": {
                "type": "HCaptchaTaskProxyLess",
                "websiteURL": "https://rbxgold.com/",
                "websiteKey": self.website_key,
                "userAgent": self.user_agent
            }
        })
        if "taskId" not in captcha_created.text:
            return False
        taskid = captcha_created.json()['taskId']
        while True:
            r = requests.post('https://api.capsolver.com/getTaskResult',
                              json={'clientKey': self.apikey, 'taskId': taskid}).json()
            if r['status'] == "ready":
                return r['solution']['gRecaptchaResponse']


auto_join = AutoJoinerHandler(APIKEY)

class rblxGoldHandler(websocket.WebSocketApp):
    def __init__(self):
        self.headers = {
            'Origin': 'https://rbxgold.com',
            'Sec-WebSocket-Key': base64.b64encode(random.randbytes(16)).decode('utf-8'),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        super().__init__(
            url="wss://api.rbxgold.com/socket.io/?EIO=4&transport=websocket",
            on_message=lambda ws, msg: self.message(ws,msg),
            on_open=lambda ws: self.open(ws),
            header=self.headers)
        self.rain_started = False

    def message(self, ws, message):
        if not all(v in globals() for v in ("x", "y", "z")): return
        message = str(message).strip()
        if "2" == message:
            ws.send("3")
        if 'rain-stream' in message:
            pattern = r'\[({.*})\]'
            msg = json.loads(re.search(pattern, message).group(1)[:-2])
            if msg['status'] == "in progress" and self.rain_started == False:
                get_rain_amt = int(msg['evAmount']) + msg['tipAmount']
                # send to webhook if you want
                self.rain_started = True
                print('rain started')
                # gets the rain amount
                captcha = auto_join.solve_captcha()
                if captcha:
                    print('solved captcha!')
                    join_game = requests.post('https://api.rbxgold.com/api/rain/rain-join',
                                              params={
                                                  'hCaptchaToken': captcha
                                              },
                                              cookies={
                                                  'SID': SID
                                              },
                                              json={},
                                              headers={
                                                  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
                                              })
                    if join_game.status_code == 200:
                        print('joined rain!')
                    else:
                        print(join_game.text, join_game.status_code)
                else:
                    print('error solving captcha or no api key.')
            elif msg['status'] == "pending" and self.rain_started == True:
                self.rain_started = False
                print('rain ended')
            else:
                pass

    def open(self, ws):
        ws.send('40')
        time.sleep(1)
        ws.send('42["rain-join"]')



r = rblxGoldHandler()
r.run_forever()

# MADE BY COXY ON DISCORD
# MADE BY COXY ON DISCORD
# MADE BY COXY ON DISCORD
# MADE BY COXY ON DISCORD
# MADE BY COXY ON DISCORD
# MADE BY COXY ON DISCORD
# MADE BY COXY ON DISCORD
