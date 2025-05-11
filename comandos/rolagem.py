from discord import app_commands, Interaction
from utils.dados import rolar_dados

@app_commands.command(name="rolar", description="Rola dados no estilo RPG. Ex: 3d6, 2d20+3, 4#d8-1 Nome")
@app_commands.describe(comando="Ex: 4d6, 2d20+3, 1#d8-1 Nome")
async def rolar(interaction: Interaction, comando: str):
    resultado = rolar_dados(comando)
    await interaction.response.send_message(resultado)

@app_commands.command(name="rolar-privado", description="Rola dados e mostra o resultado apenas para você")
@app_commands.describe(comando="Ex: 4d6, 2d20+3, 1#d8-1 Nome")
async def rolar_privado(interaction: Interaction, comando: str):
    resultado = rolar_dados(comando)
    await interaction.response.send_message(resultado, ephemeral=True)

# Função de setup para registrar os comandos
async def setup(bot):
    print("🎲 Comandos de rolagem carregados!")
    bot.tree.add_command(rolar)
    bot.tree.add_command(rolar_privado)