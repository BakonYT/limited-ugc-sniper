VERSION = "2.5.0"

try:
    import discord
    from discord.ext import commands
    import aiohttp
    import asyncio
    import os
    import traceback
    import ctypes
    import json
    import time
    import uuid
    import copy
    import datetime
    from itertools import cycle
    from pick import pick
    import rgbprint
    import math
    import logging
    import logging.config
    import hashlib
    import importlib
    import rapidjson as json
    import quart

except ModuleNotFoundError:
    import os
    try:
        from pick import pick

        install = pick(["Yes", "No"], "Modulos no instalados! Encontrados, Quieres actualizarlos?", indicator=">>")[1] == 0
    except ModuleNotFoundError:
        install = input("Modulos no instalados! Encontrados, Quieres actualizarlos? Y/N\n>> ").lower() == "y"

    if install:
        print("Los modulos requeridos no estan instalados! Instalandolos ahora...")
        os.system("python -m pip install --upgrade pip")
        os.system("pip install aiohttp"); os.system("python -m pip install aiohttp"); os.system("py -m pip install aiohttp")
        os.system("pip install pick");os.system("python -m pip install pick"); os.system("py -m pip install pick")
        os.system("pip install rgbprint");os.system("python -m pip install rgbprint"); os.system("py -m pip install rgbprint")
        os.system("pip install discord.py");os.system("python -m pip install discord.py"); os.system("py -m pip install discord.py")
        os.system("pip install python-rapidjson");os.system("python -m pip install python-rapidjson");os.system("py -m pip install python-rapidjson")
        os.system("pip install quart==0.17.0");os.system("python -m pip install quart==0.17.0");os.system("py -m pip install quart==0.17.0")
        print("Se instalaron todos los modulos necesitados!.")
    else:
        print("Abortando la instalación.")

    os.system("Pause")
    exit(1)

os.system("cls")
if not os.path.exists("./logs"): os.mkdir("./logs")
logging.basicConfig(filename=f"./logs/logs {str(datetime.datetime.now())[:-10].replace(':', '')}.txt",level=logging.INFO, format="%(asctime)s:%(levelname)s-%(module)s  %(message)s")
logging.debug("Started")

with open('config.json', "r") as f:
    conf = json.load(f)

recent_logs = []
all_logs = []

class Visual:
    @staticmethod
    def betterPrint(content, print_log=False, log=True, log_level="info", include_time=True):
        now = f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')}] " if include_time else ""
        if log:
            all_logs.append(Visual.removeColour(f"{now}{content}"))
            exec('logging.'+log_level+'(f"{content}")')
        if conf["better print"] and print_log:
            recent_logs.append(f"[COLOR_LIGHT_BLUE]{now}{content}")
            return

        if Visual.__parsegradient(content) == 0:
            print(Visual.textToColour(f"[COLOR_LIGHT_BLUE]{now}{content}"))

    @staticmethod
    def add_log(content, include_time=True):
        now = f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')}] " if include_time else ""
        all_logs.append(Visual.removeColour(f"{now}{content}"))

    @staticmethod
    def __parsehex(text):
        txt = text.split("[HEX_")
        if len(txt) == 1:
            return txt[0]

        text = txt[0]
        for i in txt[1:]:
            i = i.split("]")
            text += f"{rgbprint.Color(i[0])}{''.join(i[1:])}"

        return text

    @staticmethod
    def __parsergb(text):
        txt = text.split("[RGB_")
        if len(txt) == 1:
            return txt[0]

        text = txt[0]
        for i in txt[1:]:
            i = i.split("]")
            r, g, b = i[0].split(",")
            text += f"{rgbprint.Color((int(r), int(g), int(b)))}{''.join(i[1:])}"

        return text

    @staticmethod
    def __parsegradient(text):  
        if "[GRADIENT" not in text:
            return 0
        try:
            txt = text.split("[GRADIENT_")
            print(txt[0], end="")
            for i in txt[1:]:
                start, end = i.split("]")[0].split("_")
                toprint, other = i.split("[END]")
                toprint = "".join(toprint.split("]")[1:])
                rgbprint.gradient_print(toprint, start_color=start, end_color=end, end="")
                print(other, end="")
        except IndexError:
            Visual.betterPrint("[COLOR_RED]Syntax error whilst decoding gradients.")
            os.system("pause")
            exit(1)

        return 1

    @staticmethod
    def removeColour(text: str):
        if "COLOR" in text:
            for key in theme_info["colours"]:
                text = text.replace(key, "")

        return text

    @staticmethod
    def textToColour(text: str):
        if "COLOR" in text:
            for key in theme_info["colours"]:
                text = text.replace(key, f"\x1b[38;5;{theme_info['colours'][key]}m")

        try:
            if "[HEX" in text:
                text = Visual.__parsehex(text)
        except IndexError:
            Visual.betterPrint("[COLOR_RED]Syntax error whilst decoding hex.")
            os.system("pause")
            exit(1)

        try:
            if "[RGB" in text:
                text = Visual.__parsergb(text)
        except IndexError:
            Visual.betterPrint("[COLOR_RED]Syntax error whilst decoding RGB.")
            os.system("pause")
            exit(1)

        return text

    @staticmethod
    def textToVar(sniper, text: str):
        if type(sniper) != UGCSniper:
            Visual.betterPrint("[COLOR_RED] WARNING, NO VALID SNIPER PASSED TO textToVar")
            os.system("pause")
            exit(1)

        custom_vars = {
            "[username]": sniper.userinfo["name"],
            "[displayName]": sniper.userinfo["displayName"],
            "[userId]": sniper.userinfo["id"],

            "[proxiesEnabled]": False,
            "[proxyAmount]": len(sniper.proxies_raw),
            "[currentProxy]": sniper.proxy,
            "[changedProxies]": sniper.proxies_switched,
            "[ratelimits]": sniper.ratelimits,

            "[time]": sniper._time,
            "[limitedsAmount]": len(sniper.limiteds),
            "[limiteds]": ", ".join(sniper.limiteds)[:-2],
            "[speed]": sniper.speed,
            "[status]": sniper.stats,
            "[priceChecks]": sniper.checks_made,
            "[bought]": sniper.bought,
            "[boughtpaid]": sniper.boughtpaid,

            "[x-csrf]": sniper.cookies[0][1],
            "[cooldown]": sniper.cooldown,
            "[errors]": sniper.errors,
            "[version]": VERSION,
            "[mode]": sniper.mode,
            "[logs]": "".join(themeConfig.get('log seperator', "[LOG]\n").replace("[LOG]", log) for log in recent_logs),
            "[ip]": sniper.ip,
            "[runtime]": round(time.perf_counter(), 2)
        }

        for key in custom_vars:
            text = text.replace(key, str(custom_vars[key]))

        return text

class Other:
    @staticmethod
    def calculate_cooldown(reqs_per_min, mode):
        try:
            cooldown = 60 / reqs_per_min
        except ZeroDivisionError:
            Visual.betterPrint("[COLOR_RED]No hay limitados añadidos, Porfavor añade unos para que el sniper funcione!.")
            os.system("pause")
            exit(1)

        cooldown = conf.get(f"custom {mode} cooldown", -1) if conf.get(f"custom {mode} cooldown", -1) >= 0 else cooldown
        return cooldown

    @staticmethod
    async def handle_ratelimit(sniper, log, custom_cooldown=-1, text=""):
        cooldown = conf['proxy ratelimit cooldown'] if sniper.proxiesOn else conf['ratelimit cooldown']
        if custom_cooldown >= 0: cooldown = custom_cooldown

        if text == "": text = f"[COLOR_RED]Ratelimit continuing in {cooldown} seconds."
        Visual.betterPrint(f"{text} - {log}", True)

        await asyncio.sleep(cooldown)
        if sniper.proxiesOn:
            sniper.proxy = next(sniper.proxy_pool)
            sniper.proxies_switched += 1
            return False, [], [], True

        sniper.ratelimits += 1
        return False, [], [], True


# Load theme
with open("themes/required/required.json", "r") as f:
    theme_info = json.load(f)

themeVersion = "1.2.0"
_version = "v0"

themeLocation = "./themes/"+conf["current theme"]
with open(themeLocation + "/config.json", "r") as f:
    themeConfig = json.load(f)
if themeConfig["version"] != themeVersion:
    Visual.betterPrint(f"[COLOR_RED]Aviso! - La version del tema esta desactualizada, Tal vez no funcione.\n"
                       f"Igual quieres continuar?[COLOR_WHITE]")
    if pick(["Yes", "No"], "", indicator=themeConfig.get("indicator", ">>"))[1] == 1:
        exit(1)

if themeConfig["type"] not in theme_info["types"]:
    Visual.betterPrint(f"[COLOR_RED]Theme has invalid type, types can only be {' or'.join(theme_info['types'])[:-3]}")

if themeConfig["type"] == "py":
    with open("themes/required/whitelisted.hash", "r") as f:
            with open(f"{themeLocation}/{themeConfig['script']}", "r") as con:
                stop = hashlib.sha256(con.read().encode()).hexdigest() in f.read().split(";")

    if not conf.get("allowPyThemes", False) and not stop:
        print(Visual.textToColour("[COLOR_LIGHT_BLUE]"), end="\n")
        idx = pick(["Yes", "Yes, and dont warn me again.", "Yes, and whitelist this theme", "No", "No, and show me more information about this program"],
                   f"AVISO! El tema que vas a usar a continuación usa scripts, Quieres continuar?",
                   indicator=themeConfig.get("indicator", ">>"))[1]
        if idx == 3:
            os.system("pause")
            exit(1)
        if idx == 1:
            conf["allowPyThemes"] = True
            with open('config.json', "w") as f:
                json.dump(conf, f, indent=4)
        if idx == 2:
            with open("themes/required/whitelisted.hash", "a") as f:
                with open(f"{themeLocation}/{themeConfig['script']}", "r") as con:
                    f.write(hashlib.sha256(con.read().encode()).hexdigest()+";")
        if idx == 4:
            with open(themeLocation[2:] + "/" + themeConfig["script"], "r") as f:
                file_content = f.read()

            imports = ""
            for i in file_content.split("import "):
                imports += f"\t{i.splitlines()[0].replace('from ', '')}\n"

            print(Visual.textToColour(f"[COLOR_LIGHT_BLUE] All imports: \n{imports}\n"
                                      f"[COLOR_GREEN]Lines of code: {len(file_content.splitlines())}\n\n"
                                      f"[COLOR_WHITE]"))

            os.system("pause")
            exit(1)

    themeFile = importlib.import_module(themeLocation.replace("/", ".")[2:] + "." + themeConfig["script"][:-3])

if os.name == "nt": ctypes.windll.kernel32.SetConsoleTitleW(themeConfig["title"])
if os.name == "nt" and themeConfig.get("resize", {"width": -1, "height": -1}) != {"width": -1, "height": -1}:
    os.system(f"mode con: cols={themeConfig['resize']['width']} lines={themeConfig['resize']['height']}")

with open(f"{themeLocation}/{themeConfig['logo']}", "r", encoding="unicode_escape") as f: logo = Visual.textToColour(f.read())
with open(f"{themeLocation}/{themeConfig['printText']}", "r", encoding="unicode_escape") as f: printText = Visual.textToColour(
    f.read())

start_tasks = []
iteration_tasks = []
end_tasks = []

for module in os.listdir("./extensions"):
    if module == "required":
        continue

    contents = ""
    for script in os.listdir(f"./extensions/{module}"):
        if os.path.isdir(f"./extensions/{module}/{script}"): continue
        with open(f"./extensions/{module}/{script}", "r") as f: contents += f.read()

    module_hash = hashlib.sha256(contents.encode()).hexdigest()
    with open("./extensions/required/trustedExtensions.hash", "r") as f: trustedhashes = f.read().split(";")
    if module_hash not in trustedhashes and not conf.get("trustExtensions", False):
        print(Visual.textToColour("[COLOR_RED]"), end="")
        idx = pick(["Yes", "Yes, and dont warn me again.", "Yes, and whitelist this extension", "No"], "WARNIG - Unknown extension found. Do you want to continue?", indicator=conf.get("indicator", ">>"))[1]
        if idx == 1:
            conf["trustExtensions"] = True
            with open("config.json", "w") as f:
                json.dump(conf, f, indent=4)
        if idx == 2:
            with open("./extensions/required/trustedExtensions.hash", "a") as f:
                f.write(module_hash+";")

        if idx == 3:
            os.system("pause")
            exit(1)

    module = importlib.import_module(f"extensions.{module}")
    if hasattr(module, '__all__'):
        all_names = module.__all__
    else:
        all_names = [name for name in dir(module) if not name.startswith('_')]

    if "start" in dir(module): start_tasks.append(module.start)
    if "iteration" in dir(module): iteration_tasks.append(module.iteration)
    if "end" in dir(module): end_tasks.append(module.end)

    globals().update({name: getattr(module, name) for name in all_names})

print(Visual.textToColour(f"[COLOR_LIGHT_BLUE]El Sniper esta hecho por:Bakon#9354 (Bakon) \n"
                   f"[COLOR_LIGHT_BLUE]Unete a nuestra tripulación!: https://discord.gg/65vD6GTwtP)"))
time.sleep(5)

class UGCSniper:
    def __init__(self):
        os.system("cls" if os.name == "nt" else "clear")
        if os.name == "nt": ctypes.windll.kernel32.SetConsoleTitleW("ShapeShifter Sniper")
        if os.name == "nt": asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        # Init data
        self.errors = 0
        self._time = 0
        self.speed = 0
        self.bought = 0
        self.boughtpaid = 0
        self.checks_made = 0
        self.ratelimits = 0
        self.proxies_switched = 0
        self.stats = "N/A"
        self.proxy = "N/A"
        self.version = VERSION

        self.limiteds = []
        self.limitednames = {_id: "N/A" for _id in self.limiteds}
        self.ip = ""

        self.mode = ""
        self.mode_time = False
        self.minutes = int(conf["time wait minutes"])
        self.unix = math.floor(conf["time wait unix"])
        self.cooldown = 0

        self.userinfo = {}
        self.update_token = False
        asyncio.run(self.auto_update())
        self.get_info()

        self.load_limiteds()
        self.limitednames = {_id: "N/A" for _id in self.limiteds}

        self.load_proxies()
        self.get_type()

    def get_info(self):

        self.cookies = [[i, ""] for i in conf["cookie"]]
        if type(conf["cookie"]) != str: return
        with open(conf["cookie"], "r") as f:
            self.cookies = [[i, "", 0] for i in f.read().replace(";", "").splitlines()]

    def load_limiteds(self):
        self.limiteds = conf["limiteds"]
        if type(self.limiteds) != str:
            return
        with open(conf["limiteds"], "r") as f:
            contents = f.read()

            if "com" in contents:
                Visual.betterPrint(
                        "[COLOR_RED]Invalid id format given, please make sure its only the id not the full link.")
                os.system("pause")
                exit(0)

            self.limiteds = contents.replace(" ", "").splitlines()
            if "," in contents:
                self.limiteds = contents.replace(" ", "").split(",")

    async def check_proxies(self):
        async def is_working(session, proxy):
            '''
            :param session: The aiohttp session
            :param proxy: The proxy url

            :return: bool working
            '''
            try:
                working = await session.get("http://users.roblox.com/v1/users/authenticated", ssl=False, proxy=proxy, timeout=conf.get("timeout", 3))
                if working.status == 401:
                    resp = await session.get(f"http://ip-api.com/json/", ssl=False, proxy=proxy,
                                             timeout=conf.get("timeout", 3))
                    data = json.loads(await resp.text())

                    spacing = " " * (50-len(f"{data['country']} ({data['regionName']})"))
                    print(Visual.textToColour(f"[COLOR_GREEN][+] Working proxy in [COLOR_WHITE]{data['country']} ({data['regionName']})[COLOR_GREEN]  {spacing}Proxy: {proxy}"))

                    self.proxies_raw.append(proxy)
                    return True
            except aiohttp.client_exceptions.InvalidURL:
                new_prox = proxy.split(":")
                proxy = ""
                for idx, item in enumerate(new_prox):
                    if idx == len(new_prox)-2: proxy += "@"+item
                    elif idx == 0: proxy += item
                    else: proxy += ":"+item
                if proxy == "" or proxy == ":": return False

                return await is_working(session, proxy)
            except:
                return False

            return False

        chunks = [self.proxies_raw[i:i + 500] for i in range(0, len(self.proxies_raw), 500)]
        self.proxies_raw = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=None),
                                         json_serialize=json.dumps,
                                         trust_env=True) as s:

            for chunk in chunks:
                tasks = []
                for proxy in chunk:
                    tasks.append(asyncio.create_task(is_working(s, proxy)))

                await asyncio.gather(*tasks)

    def load_proxies(self):
        with open(conf["proxies"], "r") as f:
            self.proxies_raw = ["http://"+proxy if "http" not in proxy else proxy for proxy in f.read().splitlines()]
            self.proxiesOn = bool(self.proxies_raw) and conf["proxies enabled"]
            self.proxy = "N/A"

            if self.proxiesOn:
                if conf["checkProxies"]:
                    print(Visual.textToColour("[COLOR_LIGHT_BLUE]"), end="")
                    idx = pick(["Yes", "Yes, y guarda las proxies funcionales.", "No", "No, and don't remind me again"], "Proxys encontradas, Quieres checkearlas?", indicator=themeConfig.get('indicator', ">>"))[1]
                    if idx == 0 or idx == 1:
                        asyncio.run(self.check_proxies())
                    if idx == 1:
                        with open(conf["proxies"], "w") as f:
                            f.write("\n".join(self.proxies_raw))
                    if idx == 1 or idx == 3:
                        conf["checkProxies"] = False
                        with open("config.json", "w") as f:
                            json.dump(conf, f, indent=4)

                if len(self.proxies_raw) == 0:
                    return

                self.proxy_pool = cycle(self.proxies_raw)
                self.proxy = next(self.proxy_pool)

    async def auto_update(self):
        async with aiohttp.ClientSession() as s:
            try: self.ip = json.loads(await (await s.get("http://www.httpbin.org/ip", timeout=2)).text())["origin"]
            except: self.ip = "N/A"

        if not conf["auto update"] or conf.get("update reminder", 0) > time.time():
            return
        Visual.betterPrint("[COLOR_AQUAMARINE_1A]Revisando por actualizaciones potenciales!...")
        async with aiohttp.ClientSession() as s:
            src = await (await s.get("https://github.com/BakonYT/limited-ugc-sniper/blob/main/main.py")).text()
        try: version = src.split("VERSION = \"")[1].split("\"")[0]
        except: version = VERSION
        if version != VERSION:
            idx =  pick(["Yes", "No", "No, y no avisar mas", "No, Avisame en 30 minutos"], Visual.textToColour("Nueva actualización, quieres continuar?"), indicator=themeConfig.get("indicator", ">>"))[1]
            if idx == 1:
                return
            if idx == 2:
                conf["auto update"] = False
                with open('config.json', "w") as f:
                    json.dump(conf, f, indent=4)
                return
            if idx == 3:
                conf["updateReminder"] = math.floor(time.time())+30*60
                with open('config.json', "w") as f:
                    json.dump(conf, f, indent=4)
                return
            Visual.betterPrint("[COLOR_AQUAMARINE_1A]Actualizando codigo...")
            with open("main.py", "w") as f: f.write(src)
            Visual.betterPrint("[COLOR_AQUAMARINE_1A]Codigo actualizado! Reinicia el sniper para usar la version mas nueva!")
            os.system("pause")
            exit(0)
        else:
            Visual.betterPrint("[COLOR_AQUAMARINE_1A]No hay actualizaciones!.")

    def get_type(self):
        modes = ["Velocidad 1-10 Minutos Antes!", "Casual 10-60 Minutos Antes!", "Afk 1-12 Horas Antes!", "Time 1-∞ Minutos Antes!", "Tiempo especifico 1-∞ Minutos Antes!", "Checkeo de UGC en venta! para revender"]
        modeNames = ["Velocidad", "Casual", "Afk", "Tiempo", "Tiempo especifico", "Checkeo de reventa de limitados"]

        self.mode = conf.get("mode", "").title()
        if self.mode not in modeNames:
            self.mode = modeNames[pick(modes, "Seleciona el modo!: ", indicator=themeConfig.get("indicator", ">>"))[1]]

        if self.mode == "Velocidad":
            self.cooldown = Other.calculate_cooldown(60, self.mode.lower())

        elif self.mode == "Casual":
            self.cooldown = Other.calculate_cooldown(55, self.mode.lower())

        elif self.mode == "Afk":
            self.cooldown = Other.calculate_cooldown(50, self.mode.lower())

        elif self.mode == "Tiempo":
            self.mode_time = True
            if self.minutes < 0:
                Visual.betterPrint("[COLOR_LIGHT_BLUE][>>] Pon la cantidad de minutos mientras el ugc sale!: ")
                self.minutes = int(input(Visual.textToColour("[COLOR_LIGHT_BLUE]   [>>] ")))
            Visual.betterPrint(f"[COLOR_VIOLET][*] Sniper correra {self.minutes} minutes / {self.minutes * 60} segundos antes de snipear!")
            time.sleep(3)

            self.cooldown = conf["Tiempo perzonalizado cooldown"] if conf["Tiempo perzonalizado cooldown"] >= 0 else 0.5
            if len(self.limiteds) == 0:
                Visual.betterPrint("[COLOR_RED]No hay limitados añadidos, porfavor añade un limitado para que el sniper funcione!.")
                os.system("pause")
                exit(1)
        elif self.mode == "Resellable Check":

            async def main(id, xcsrf):
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://inventory.roblox.com/v1/users/{id}/can-view-inventory") as response:
                        
                        data = await response.json()
                        if data["canView"] == False:
                            print("El inventario del usuario es privado! - parando")
                            return
                        else:
                         async with session.get(f"https://inventory.roblox.com/v2/users/{id}/inventory/8?limit=100&sortOrder=Desc", cookies={".ROBLOSECURITY": self.cookies[-1][0]}) as response:            
                            data = await response.json()
                            for item in data["data"]:
                                if item["collectibleItemId"] != None:
                                    print(f"Found {item['assetName']} - ({item['assetId']}) --- Checking if asset is resellable")
                                    async with session.post(f"https://catalog.roblox.com/v1/catalog/items/details", headers={"X-CSRF-TOKEN": xcsrf}, cookies={".ROBLOSECURITY": self.cookies[-1][0]}, json={"items": [{"itemType": "Asset", "id": int(item['assetId'])}]}) as response:
                                        data = await response.json()
                                        if data["data"][0]["hasResellers"] == True:
                                            print(f"Resellable asset: {item['assetName']} - ({item['assetId']})")
                                
                                        else:
                                            continue

            async def get_token(self):
                async with aiohttp.ClientSession(json_serialize=json.dumps) as s:
                    self.userinfo = await (await s.get("https://users.roblox.com/v1/users/authenticated", cookies={".ROBLOSECURITY": self.cookies[-1][0]})).json()
                    try: self.cookies[-1][2] = self.userinfo["id"]
                    except KeyError:
                        Visual.betterPrint("[COLOR_RED]Cookie invalida!.")
                        os.system("pause")
                        exit(1)

                    for idx, cookie in enumerate(self.cookies[1:]):
                        self.cookies[idx][2] = (await (await s.get("https://users.roblox.com/v1/users/authenticated",
                             cookies={".ROBLOSECURITY": cookie[0]}, ssl=False)).json())['id']

                    while 1:
                        for idx, cookie in enumerate(self.cookies):
                            if idx == 0 and self.update_token: self.update_token = False
                            resp = await s.post("https://auth.roblox.com/v2/logout",
                                        cookies={".ROBLOSECURITY": cookie[0]}, ssl=False)
                            self.cookies[idx][1] = resp.headers['x-csrf-token']

                            return self.cookies[idx][1]

            async def get_userId():
                async with aiohttp.ClientSession(json_serialize=json.dumps) as s:
                    for idx, cookie in enumerate(self.cookies):
                        self.cookies[idx][2] = (await (await s.get("https://users.roblox.com/v1/users/authenticated",
                             cookies={".ROBLOSECURITY": cookie[0]}, ssl=False)).json())['id']
                    return self.cookies[idx][2]
                    

            async def combine(self):
                print("Empezando el checkeo de resell de limitados")
                userid = await get_userId()
                xtoken = await get_token(self)
                
                await main(userid, xtoken)
                exit(0)

            asyncio.run(combine(self))
        else:
            while 1:
                if self.unix < 0:
                    Visual.betterPrint("[COLOR_LIGHT_BLUE][>>] Pon el tiempo de cuando el limitado saldra.")
                    self.unix = math.floor(float(input(Visual.textToColour("[COLOR_LIGHT_BLUE]   [>>] "))))
                self.minutes = math.floor((self.unix - time.time())/60)
                if self.minutes < 0:
                    Visual.betterPrint("[COLOR_RED]Aviso! El tiempo ya ha pasado!, Porfavor pon un tiempo valido!.")
                    time.sleep(1)
                    self.unix = -1
                    os.system("cls" if os.name == "nt" else "clear")
                    continue
                break

            Visual.betterPrint(f"[COLOR_LIGHT_BLUE]Empezara a snipear en {self.minutes} minutos {datetime.datetime.fromtimestamp(self.unix)}")
            time.sleep(3)
            self.mode_time = True
            self.cooldown = conf["custom unix cooldown"] if conf["custom unix cooldown"] >= 0 else 0.5

    async def wait(self):
        if self.mode_time is not True:
            return
        Visual.betterPrint(
            "[COLOR_AQUAMARINE_1A]Tu has elejido tiempo. Siente el poder de conseguir limitados poderosos!. Con la maravillosa fortuna que puedes hacer, solamente esperando!..")
        Visual.betterPrint(f"[COLOR_PINK_1][*] You have {self.minutes} minutes left.")

        async with aiohttp.ClientSession() as s:
            for i in range(self.minutes):
                fact = json.loads(await (await s.get("https://catfact.ninja/fact")).text())["fact"]
                await asyncio.sleep(60)
                Visual.betterPrint(f"[COLOR_PINK_1][*] Te quedan {self.minutes - (i + 1)} Minutos .\n"
                                   f"\t[COLOR_CYAN]Random cat fact: {fact}")

        Visual.betterPrint(f"[COLOR_PINK_1][*] El tiempo acabo!, empezando a spamear el snipe")

    def start(self):
        for task in start_tasks: task()
        asyncio.run(self.main())

    async def print_all(self):
        global recent_logs
        iteration = 0
        if themeConfig["type"] == "txt": Visual.betterPrint(logo, log=False)
        if themeConfig["type"] == "py":
            if themeFile.printLogo() == 0:
                sniper.errors += 1

        while 1:
            if iteration > conf.get("log reset iteration", 3):
                iteration = 0
                recent_logs = []

            os.system("cls" if os.name == "nt" else "clear")
            if themeConfig["type"] == "py":
                if conf.get("logo dupe", True):
                    if themeFile.printLogo() == 0: sniper.errors += 1

                if themeFile.printText(sniper, "".join(themeConfig.get('log seperator', "[LOG]\n").replace("[LOG]", log) for log in recent_logs)) == 0:
                    sniper.errors += 1

            if themeConfig["type"] == "txt":
                if conf.get("logo dupe", True): Visual.betterPrint(logo, log=False, include_time=False)
                Visual.betterPrint(Visual.textToVar(self, printText), log=False, include_time=False)

            await asyncio.sleep(conf["print update cooldown"])
            iteration += 1

    async def debug_print(self):
        global recent_logs

        Visual.betterPrint("[COLOR_GREEN]Correctamente empezando el token!")
        while 1:
            if recent_logs:
                Visual.betterPrint("\n".join(recent_logs), include_time=False)
                recent_logs = []
            await asyncio.sleep(0.1)

    async def get_token(self):
        logging.info("Empezando a obtener el token")

        async with aiohttp.ClientSession(json_serialize=json.dumps) as s:
            self.userinfo = await (await s.get("https://users.roblox.com/v1/users/authenticated",
                             cookies={".ROBLOSECURITY": self.cookies[-1][0]})).json()
            try: self.cookies[-1][2] = self.userinfo["id"]
            except KeyError:
                Visual.betterPrint("[COLOR_RED]Invalid cookie parsed.")
                os.system("pause")
                exit(1)

            for idx, cookie in enumerate(self.cookies[1:]):
                self.cookies[idx][2] = (await (await s.get("https://users.roblox.com/v1/users/authenticated",
                             cookies={".ROBLOSECURITY": cookie[0]}, ssl=False)).json())['id']

            while 1:
                for idx, cookie in enumerate(self.cookies):
                    if idx == 0 and self.update_token: self.update_token = False

                    resp = await s.post("https://auth.roblox.com/v2/logout",
                                        cookies={".ROBLOSECURITY": cookie[0]}, ssl=False)
                    self.cookies[idx][1] = resp.headers['x-csrf-token']
                    logging.info(f"Got token of {self.cookies[idx][1]}")

                    for _ in range(round(120/len(self.cookies))):
                        if self.update_token:
                            break
                        await asyncio.sleep(1)

    async def get_stock(self, session, limited):
        try:
            info = await session.post("https://catalog.roblox.com/v1/catalog/items/details",
                          json={"items": [{"itemType": "Asset", "id": int(limited)}]}, ssl=False, proxy=self.proxy if self.proxiesOn else "", proxy_auth=None, timeout=conf.get("timeout", 3))
        except asyncio.exceptions.TimeoutError:
                self.proxy = next(self.proxy_pool)
                self.proxies_switched += 1
        except:
            Visual.betterPrint('[COLOR_RED]Fallado obteniendo el stock', True, log_level="warning")
            self.errors += 1
            return 1

        try:
            left = json.loads(await info.text())["data"][0]["unitsAvailableForConsumption"]
        except (KeyError, json.JSONDecodeError):
            Visual.betterPrint(f"[COLOR_RED]Fallado obteniendo el stock!. Full log: {await info.text()} - {info.reason}", True)
            return 1

        return left

    async def __buy(self, session, buydata, liminfo):
        '''
        :param session: The aiohttp.ClientSession
        :param buydata: The data needed for the buy request

        :return: bool bought, bool ratelimit, bool switch_cookie, bool soldout, dict data
        '''

        try:
            req = await session.post(
            f"https://apis.roblox.com/marketplace-sales/v1/item/{buydata['collectibleItemId']}/purchase-item",
            json=buydata, ssl=False, proxy=self.proxy if self.proxiesOn and conf["purchase proxy"] else "", timeout=conf.get("timeout", 3), proxy_auth=None)
        except asyncio.exceptions.TimeoutError:
            Visual.betterPrint("[COLOR_RED]Compra ratelimit encontrado! (timeout)", True)
            return False, True, False, False, {}

        if req.reason == "Too Many Requests":
            Visual.betterPrint("[COLOR_RED]Compra ratelimit encontrado!", True)
            return False, True, False, False, {}

        data_raw = await req.text()
        if data_raw == "":
            Visual.betterPrint("[COLOR_RED]Se encontro un error mientras se obtenia la información de compra!", True, log_level="warning")
            self.errors += 1
            return False, False, False, False, {}

        try: data = json.loads(data_raw)
        except json.JSONDecodeError:
            Visual.betterPrint(f"[COLOR_RED]Se encontro un error mientras obteniendo la información de compra del producto. Info: '{data_raw}' - {req.reason}", True, log_level="warning")
            self.errors += 1
            return False, False, False, False, {}
        if data['purchaseResult'] == 'Flooded':
            Visual.betterPrint(f"[COLOR_GREEN]Se compro cantidad maxima de items en esta cuenta. Cambiando cookies", True)
            return False, False, True, False, data

        if data['errorMessage'] == 'QuantityExhausted':
            Visual.betterPrint(f"[COLOR_RED]Todos los items fueron vendidos!.", True)
            return False, False, False, True, data

        if not data["purchased"]:
            Visual.betterPrint(f"[COLOR_RED]Fallo en comprar limitado, intentando de nuevo!.. Info: {data} - {buydata}", True)
            return True, False, False, False, data

        if data["purchased"]:
            Visual.betterPrint(f"[COLOR_AQUAMARINE_1A]Successfully bought limited! Info: {data} - {buydata}", True)
            if conf["webhook enabled"]:
                embed = discord.Embed(title='Purchased Limited', description='You successfully sniped a limited!',
                                      color=discord.Colour().blue())
                embed.add_field(name=f'Item',
                                      value=f'[{liminfo["name"]}](https://www.roblox.com/catalog/{liminfo["id"]})')
                embed.add_field(name=f'Stock', value=f'{liminfo["unitsAvailableForConsumption"]}')
                embed.add_field(name=f'Recieved', value=f'{data}')

                webhook = discord.Webhook.from_url(conf["webhook"], session=session)
                await webhook.send(embed=embed)

            self.bought += 1
            return True, False, False, False, data

        return False, False, False, False, data

    async def buy(self, session, data, dont_remove=False):
        '''
        :param session: The aiohttp session
        :param data: The item information recieved by the request

        :return: bool boughtsession
        '''
        if dont_remove is False:
            try: self.limiteds.remove(str(data["id"]))
            except ValueError: return

        # Get the product id
        productid = None
        Visual.betterPrint("Obteniendo información necesitada!...", True)
        while productid is None:
            _inf = await session.post("https://apis.roblox.com/marketplace-items/v1/items/details",
                           json={"itemIds": [data["collectibleItemId"]]}, ssl=False)

            try:
                Visual.betterPrint("Sent request for information, scraping needed information")
                inf = json.loads(await _inf.text())[0]
                productid = inf["collectibleProductId"]

            except (json.JSONDecodeError, KeyError):
                Visual.betterPrint(
                    f"[COLOR_RED]Algo salio mal mientras obteniendo los logs - {await _inf.text()} - {_inf.reason}. Intentando nuevamente en 1 segundo", True)
                await asyncio.sleep(1)
                continue

        # Paid checks
        if inf["price"] > 0 and conf.get("purchase paid ugcs", False):
            Visual.betterPrint(f"[COLOR_RED]Aborto el comprar un limitado. Razon: Limitado pago! - Precio: {inf['price']}", True)
            return
        if inf["price"] > conf.get("paid ugcs max price", 0):
            Visual.betterPrint(f"[COLOR_RED]Aborto el comprar un limitado. Razon: Precio del item muy caro - Precio: {inf['price']}", True)
            return
        if inf["price"] > 0 and self.boughtpaid >= conf.get("purchase paid ugcs amount", 0):
            Visual.betterPrint(f"[COLOR_RED]Aborto el comprar un limitado. Razon: Maxima cantidad de limitados pagos comprados. - Precio: {inf['price']}",
                               True)
            return

        Visual.betterPrint("Got needed information, setting up data", True)
        buydata = {
            "collectibleItemId": inf["collectibleItemId"],
            "expectedCurrency": 1,
            "expectedPrice": data["price"] if conf.get("purchase paid ugcs", False) else 0,
            "expectedPurchaserId": "id of the reciever",
            "expectedPurchaserType": data["creatorType"],
            "expectedSellerId": data["creatorTargetId"],
            "expectedSellerType": "User",
            "idempotencyKey": "random uuid4 string that will be your key or smthn",
            "collectibleProductId": productid
        }
        Visual.betterPrint("Set up data.", True)
        boughtsession = 0

        soldout = False
        while not soldout:
            for cookie in self.cookies:
                buydata['expectedPurchaserId'] = cookie[2]
                session.cookie_jar.update_cookies({".ROBLOSECURITY": cookie[0]})
                session.headers["x-csrf-token"] = cookie[1]

                if soldout:
                    break

                while not soldout:
                    tasks = []

                    for _ in range(4):
                        buydata["idempotencyKey"] = str(uuid.uuid4())
                        tasks.append(asyncio.create_task(self.__buy(session, copy.copy(buydata), data)))
                    instock = asyncio.create_task(self.get_stock(session, data["id"]))

                    for task in tasks:
                        task = await task
                        if task[0]:
                            boughtsession += 1
                        if task[1]:
                            Visual.betterPrint("[COLOR_RED]Entramos en un rate limit Continuando en 0.1 segundo..", True)
                            self.ratelimits += 1
                            await asyncio.sleep(0.1)
                        if task[2]:
                            boughtsession += 4
                            if inf["price"] > 0:
                                self.boughtpaid += 1
                                if self.boughtpaid >= conf.get("compra ugc limitados pagos", 0):
                                    Visual.betterPrint(
                                        f"[COLOR_RED]Abortado comprar un limitado. Razon: Maxima cantidad de ugc limitados pagos comprados.", True)
                                    return boughtsession
                        if task[3]:
                            soldout = True

                    if boughtsession >= 4:
                        boughtsession = 0
                        break

                    if await instock < 1:
                        Visual.betterPrint(f"Todos los items por el limitado {data['id']} Se vendieron!!", True)
                        soldout = True

        Visual.betterPrint(f"Todos los items comprados, fuera de stock, Comprando {boughtsession} limiteds", True)
        return boughtsession

    async def is_onsale(self, session: aiohttp.ClientSession, limiteds):
        '''
        :param session: aiohttp session
        :param limiteds: All the limiteds to get the info of.

        :return: bool item_on_sale, list resp_data, list all_data, bool skip_wait
        '''
        if len(limiteds) == 0:
            return False, [], [], False

        item_on_sale = False
        resp_data = []
        try:
            resp = await session.post("http://catalog.roblox.com/v1/catalog/items/details",
                            json={"items": [{"itemType": "Asset", "id": int(limited)} for limited in limiteds]}, ssl=False, proxy=self.proxy if self.proxiesOn else "", timeout=conf.get("timeout", 3), proxy_auth=None)
        except (asyncio.exceptions.TimeoutError, aiohttp.client_exceptions.ClientHttpProxyError,
                aiohttp.client_exceptions.ClientOSError):
            return await Other.handle_ratelimit(sniper, [], 0 if not self.proxiesOn else -1, "[COLOR_RED]Error de NETWORK, Continunando. Severidad: Muy baja")

        dat = {}
        try:
            dat = json.loads(await resp.text())
            all_data = dat["data"]
        except (json.JSONDecodeError, KeyError):
            if dat.get("message", "") == "Validación de token fallo!": self.update_token = True
            return await Other.handle_ratelimit(sniper, await resp.text())

        for limited in all_data:
            if limited.get("collectibleItemId", "") != "":
                item_on_sale = True
                resp_data.append(limited)

        for i in all_data:
            self.limitednames[str(i['id'])] = i['name']
        return item_on_sale, resp_data, all_data, False


    async def main(self):
        if conf.get("bot enabled", False) is True and conf.get("bot token", "") != "":
            bot = Bot(self)
            asyncio.create_task(bot.start_bot())
            
        asyncio.create_task(self.get_token())

        await self.wait()

        while self.cookies[-1][1] == "": await asyncio.sleep(0.01)
        if conf.get("debug", False) is True:
            asyncio.create_task(self.debug_print())
        else:
            asyncio.create_task(self.print_all())

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=None),
                                         json_serialize=json.dumps,
                                         trust_env=True,
                                         cookies={".ROBLOSECURITY": self.cookies[-1][0]},
                                         headers={"x-csrf-token": self.cookies[-1][1]}) as s:

            while 1:
                start = time.perf_counter()
                for task in iteration_tasks: task()
                if s.headers["x-csrf-token"] != self.cookies[-1][1]: s.headers["x-csrf-token"] = self.cookies[-1][1]
                self.stats = themeConfig.get("status check", "Revisando limitados en venta!")

                data = await self.is_onsale(s, self.limiteds)
                self.checks_made += len(self.limiteds)

                if data[0]:
                    for limited in data[1]:
                        Visual.betterPrint(f"[COLOR_CYAN]Comprando el {limited['name']} ({limited['id']})[COLOR_WHITE]")
                        self.stats = themeConfig.get("status buying", "Comprando limitado!")

                        await self.buy(s, limited)

                self._time = round(time.perf_counter()-start, 3)
                if self._time < self.cooldown and not data[3]:
                    await asyncio.sleep(self.cooldown-self._time)

                self.speed = round(time.perf_counter()-start, 3)


if __name__ == '__main__':
    sniper = UGCSniper()
    try:
        sniper.start()
    except:
        logging.error(f"Error log: {traceback.format_exc()}")
        Visual.betterPrint("[COLOR_RED]"+traceback.format_exc())
        os.system("pause")
    finally:
        for task in end_tasks: task()
