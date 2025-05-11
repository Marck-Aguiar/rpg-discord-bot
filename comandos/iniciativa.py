import discord
from discord import app_commands, Interaction, Embed
from modais.iniciativa_modal import IniciativaModal
from utils.iniciativa_utils import gerar_embed_iniciativa

# Armazena iniciativas por canal
iniciativas_por_canal = {}

def get_dados_canal(interaction: Interaction):
    return iniciativas_por_canal.setdefault(interaction.channel_id, {"personagens": {}, "ordem": "desc"})

# Comando: registrar ou adicionar iniciativa
@app_commands.command(name="iniciativa", description="Registrar ou adicionar personagens à iniciativa")
async def iniciativa(interaction: Interaction):
    await interaction.response.send_modal(IniciativaModal(iniciativas_por_canal))

# Comando: mostrar iniciativa
@app_commands.command(name="mostrar-iniciativa", description="Mostra a ordem de iniciativa")
async def mostrar_iniciativa(interaction: Interaction):
    dados = iniciativas_por_canal.get(interaction.channel_id)

    if not dados or not dados["personagens"]:
        if not interaction.response.is_done():
            await interaction.response.send_message("⚠️ Nenhuma iniciativa registrada ainda.", ephemeral=True)
        else:
            await interaction.followup.send("⚠️ Nenhuma iniciativa registrada ainda.", ephemeral=True)
        return

    embed = gerar_embed_iniciativa(dados)
    await interaction.response.send_message(embed=embed)

# Comando: editar iniciativa
@app_commands.command(name="editar-iniciativa", description="Edita a iniciativa de um personagem")
@app_commands.describe(nome="Nome do personagem", nova_iniciativa="Novo valor de iniciativa")
async def editar_iniciativa(interaction: Interaction, nome: str, nova_iniciativa: int):
    dados = get_dados_canal(interaction)

    if nome not in dados["personagens"]:
        await interaction.response.send_message(f"⚠️ Personagem `{nome}` não encontrado.", ephemeral=True)
        return

    dados["personagens"][nome] = nova_iniciativa
    await interaction.response.send_message(f"✏️ Iniciativa de `{nome}` atualizada para `{nova_iniciativa}`.")

@editar_iniciativa.autocomplete("nome")
async def autocomplete_editar(interaction: Interaction, current: str):
    dados = iniciativas_por_canal.get(interaction.channel_id, {}).get("personagens", {})
    return [
        app_commands.Choice(name=nome, value=nome)
        for nome in dados
        if current.lower() in nome.lower()
    ]

# Comando: remover iniciativa
@app_commands.command(name="remover-iniciativa", description="Remove um personagem da iniciativa")
@app_commands.describe(nome="Nome do personagem")
async def remover_iniciativa(interaction: Interaction, nome: str):
    dados = get_dados_canal(interaction)

    if nome not in dados["personagens"]:
        await interaction.response.send_message(f"⚠️ Personagem `{nome}` não encontrado.", ephemeral=True)
        return

    del dados["personagens"][nome]
    await interaction.response.send_message(f"❌ Personagem `{nome}` removido da iniciativa.")

@remover_iniciativa.autocomplete("nome")
async def autocomplete_remover(interaction: Interaction, current: str):
    dados = iniciativas_por_canal.get(interaction.channel_id, {}).get("personagens", {})
    return [
        app_commands.Choice(name=nome, value=nome)
        for nome in dados
        if current.lower() in nome.lower()
    ]

# Comando: limpar iniciativa
@app_commands.command(name="limpar-iniciativa", description="Limpa a lista de iniciativa do canal atual")
async def limpar_iniciativa(interaction: Interaction):
    iniciativas_por_canal.pop(interaction.channel_id, None)
    await interaction.response.send_message("🧹 Lista de iniciativas foi limpa!", ephemeral=True)

# Setup
async def setup(bot):
    print("🎲 Comandos de iniciativa carregados!")
    bot.tree.add_command(iniciativa)
    bot.tree.add_command(mostrar_iniciativa)
    bot.tree.add_command(editar_iniciativa)
    bot.tree.add_command(remover_iniciativa)
    bot.tree.add_command(limpar_iniciativa)
