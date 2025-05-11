import discord
from discord import Embed

def gerar_embed_iniciativa(dados: dict) -> Embed:
    ordem = dados["ordem"]
    personagens = dados["personagens"]
    lista = sorted(personagens.items(), key=lambda x: x[1], reverse=(ordem == "desc"))

    embed = Embed(
        title="🧭 Ordem de Iniciativa",
        description=f"Ordem (**{'maior → menor' if ordem == 'desc' else 'menor → maior'}**)",
        color=discord.Color.purple()
    )

    for nome, valor in lista:
        embed.add_field(name=nome, value=f"`{valor}`", inline=False)

    return embed
