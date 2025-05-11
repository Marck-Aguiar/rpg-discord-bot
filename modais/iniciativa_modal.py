import discord
from utils.iniciativa_utils import gerar_embed_iniciativa

class IniciativaModal(discord.ui.Modal, title="Registrar ou Adicionar Iniciativas"):
    def __init__(self, iniciativas_por_canal):
        super().__init__()
        self.iniciativas_por_canal = iniciativas_por_canal

    personagens = discord.ui.TextInput(
        label="Personagens e iniciativas",
        style=discord.TextStyle.paragraph,
        placeholder="Ex: Marcus 18, Ana 12, Goblin 15",
        required=True,
        max_length=500
    )

    ordenacao = discord.ui.TextInput(
        label="Ordem (asc ou desc)",
        placeholder="desc (maior para menor) ou asc",
        required=False,
        default="desc",
        max_length=4
    )

    async def on_submit(self, interaction: discord.Interaction):
        texto = self.personagens.value
        ordem = self.ordenacao.value.lower().strip()
        if ordem not in ["asc", "desc"]:
            ordem = "desc"

        personagens = []
        for item in texto.split(','):
            partes = item.strip().rsplit(' ', 1)
            if len(partes) == 2 and partes[1].isdigit():
                nome, valor = partes[0], int(partes[1])
                personagens.append((nome, valor))

        if not personagens:
            await interaction.response.send_message("❌ Nenhuma iniciativa válida encontrada.", ephemeral=True)
            return

        canal_id = interaction.channel_id
        dados = self.iniciativas_por_canal.setdefault(canal_id, {"personagens": {}, "ordem": ordem})
        dados["ordem"] = ordem

        for nome, valor in personagens:
            dados["personagens"][nome] = valor

        embed = gerar_embed_iniciativa(dados)

        await interaction.response.send_message(
            content="✅ Personagens registrados ou atualizados com sucesso!",
            embed=embed,
            ephemeral=False
        )
