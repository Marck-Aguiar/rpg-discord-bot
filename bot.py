import discord
from discord import app_commands
from utils.dados import rolar_dados


class MeuPrimeiroBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        from comandos import iniciativa, rolagem, ppt, magias, itens, condicoes_dnd

        await iniciativa.setup(self)
        await rolagem.setup(self)
        await ppt.setup(self)
        await magias.setup(self)
        await itens.setup(self)
        await condicoes_dnd.setup(self)

        await self.tree.sync()

    async def on_ready(self):
        print(f"✅ Bot conectado como {self.user}.")

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.content.startswith("!"):
            comando = message.content[1:]
            resultado = rolar_dados(comando)
            await message.channel.send(resultado)

bot = MeuPrimeiroBot()
