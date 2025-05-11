import discord
from discord import app_commands, Interaction, Embed

escolhas = {}

# Emojis para cada opção
EMOJIS = {
    "pedra": "✊",
    "papel": "🖐️",
    "tesoura": "✌️"
}

def determinar_vencedor(jogador1, escolha1, jogador2, escolha2):
    regras = {
        ("pedra", "tesoura"): jogador1,
        ("tesoura", "papel"): jogador1,
        ("papel", "pedra"): jogador1,
        ("tesoura", "pedra"): jogador2,
        ("papel", "tesoura"): jogador2,
        ("pedra", "papel"): jogador2,
    }

    if escolha1 == escolha2:
        return "Empate! Ambos escolheram a mesma coisa."
    else:
        vencedor = regras.get((escolha1, escolha2))
        return f"O vencedor é {vencedor}! :trophy:"

# Autocomplete para a opção do jogo
async def autocomplete_opcao(
    interaction: Interaction,
    current: str
) -> list[app_commands.Choice[str]]:
    opcoes = ["pedra", "papel", "tesoura"]
    return [
        app_commands.Choice(name=f"{EMOJIS[o]} {o.title()}", value=o)
        for o in opcoes if current.lower() in o
    ]

@app_commands.command(name="jogo-ppt", description="Joga Pedra, Papel ou Tesoura contra outro jogador")
@app_commands.describe(opcao="Escolha entre pedra, papel ou tesoura")
@app_commands.autocomplete(opcao=autocomplete_opcao)
async def jogo_ppt(interaction: Interaction, opcao: str):
    jogador = interaction.user

    if opcao not in ["pedra", "papel", "tesoura"]:
        await interaction.response.send_message("Escolha inválida! Use `pedra`, `papel` ou `tesoura`.", ephemeral=True)
        return

    if jogador.id in escolhas:
        await interaction.response.send_message("Você já escolheu! Aguarde o outro jogador.", ephemeral=True)
        return

    escolhas[jogador.id] = opcao

    if len(escolhas) == 2:
        jogadores = list(escolhas.items())
        jogador1_id, escolha1 = jogadores[0]
        jogador2_id, escolha2 = jogadores[1]

        jogador1_user = await interaction.client.fetch_user(jogador1_id)
        jogador2_user = await interaction.client.fetch_user(jogador2_id)

        resultado = determinar_vencedor(jogador1_user.name, escolha1, jogador2_user.name, escolha2)

        embed = Embed(
            title="🧩 Pedra, Papel, Tesoura",
            description=(
                f"{jogador1_user.mention} escolheu **{EMOJIS[escolha1]} {escolha1}**\n"
                f"{jogador2_user.mention} escolheu **{EMOJIS[escolha2]} {escolha2}**\n\n"
                f"**Resultado:** {resultado}"
            ),
            color=discord.Color.purple()
        )

        await interaction.channel.send(embed=embed)
        escolhas.clear()
    else:
        await interaction.response.send_message("Escolha registrada! Aguardando o outro jogador...", ephemeral=True)

# 👇 Setup para registrar o comando
async def setup(bot):
    print("✊🖐✌️ Comando Pedra, Papel ou Tesoura carregado!")
    bot.tree.add_command(jogo_ppt)
