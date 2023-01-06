from pyrogram.types import Message
from pyrogram import Client
import aiohttp
import aiohttp_socks
from json import loads

print("Iniciando...")

API_ID = 16356512
API_HASH = "3be954be110a796e8c0b18f3604a5f2c"
BOT_TOKEN = "5959919695:AAH4mCZhY0wRBdi9p7eFaUbH1UOoIctuN-E"
PROXY = {}
bot = Client("delete",api_id=API_ID,api_hash=API_HASH,bot_token=BOT_TOKEN)

@bot.on_message()
async def message_handler(client: Client, message: Message):
    text = message.text
    username = message.from_user.username
    firstname = message.from_user.first_name
    usernameid = message.from_user.id
    
    print(PROXY)
    if message.document:
        try:
            proxy = PROXY[username]
        except:
            await message.reply("**No tiene /proxy guardado imposible borrar...**")
            return
        txt = await message.download()
        msg = await message.reply("✔ Enlaces extraidos!")
        
        with open(txt,"r") as tx:
            lines = tx.read().split("\n")
            
            deleted = 0
            total = len(lines)-1
            connector = aiohttp_socks.ProxyConnector.from_url(proxy)
            session = aiohttp.ClientSession(connector=connector)
            for line in lines:
                if not "http" in line:continue
                n = line.split("/")[-1]
                url = f"https://educa.uho.edu.cu/ci_portal_uho/index.php/recursos_pre/my_grocery_recursos_pred/delete_file/archivo/{n}?_=1670274909872"
                resp = await session.get(url)
                if loads(await resp.text())["success"]:
                    deleted+=1
            if total == deleted:
                await msg.edit("✔ Todos los enlaces borrados!")
            else:
                await msg.edit("✖ No se borraron todos los enlaces por algun motivo reenvie nuevamente el txt")
                return
                
    if text.startswith("/start"):
        await client.send_message(usernameid,f"__✌ Saludos {firstname}\n🌐 Bienvenido a EducaCleaner__\n\n❓ __EducaCleaner es un bot que permitira eliminar links de educa para asi ayudar a cuidar mas esa maravillosa nube\n❗ Para utilizar EducaCleaner y eliminar enlaces/links de  educa solo es necesario configurar el proxy y enviar el txt que desea eliminar__\n\nDesarrollador(es):\n**@anonedev**\n**@Yama_Tsukami**\n__**By_Ultra_FAST**")
    
    if text.startswith("/proxy"):
        try:
            proxy = text.split(" ")[1]
        except:
            await message.reply("**Forma correcta:**\n**/proxy socks5://102.45.27.9:8080**")
            return
        try:
            PROXY[username]
        except:
            PROXY[username] = ""
        PROXY[username] = proxy
        await client.send_message(usernameid,f"✔ Proxy guardado!")
        return

print("Iniciado!")
bot.run()

#Powered by Ultra_Fast