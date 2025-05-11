import discord
from discord import app_commands, Interaction, Embed
from discord.ui import Select, View, Button
from utils.condicoes_dnd_data import condicoes
import unicodedata

MAX_OPTIONS = 25

def remover_acentos(texto):
    return unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('ascii')

# ===== SELECT DE CONDIÇÃO =====
class CondicaoSelect(Select):
    def __init__(self, condicoes_pagina, condicoes_total, user, offset=0):
        options = [
            discord.SelectOption(
                label=c["nome"][:100],
                value=str(i + offset)
            ) for i, c in enumerate(condicoes_pagina)
        ]

        super().__init__(placeholder="Escolha uma condição para ver os detalhes", options=options)
        self.condicoes_total = condicoes_total
        self.user = user

    async def callback(self, interaction: Interaction):
        condicao_index = int(self.values[0])
        condicao = self.condicoes_total[condicao_index]

        embed = Embed(
            title=condicao["nome"],
            description=condicao["descricao"],
            color=discord.Color.orange()
        )

        await interaction.channel.send(
            f"{self.user.mention} escolheu **{condicao['nome']}**!",
            embed=embed
        )
        await interaction.response.defer()


# ===== VIEW DE PAGINAÇÃO =====
class CondicoesView(View):
    def __init__(self, condicoes, user, page=0):
        super().__init__(timeout=None)
        self.condicoes = sorted(condicoes, key=lambda c: c["nome"])
        self.user = user
        self.page = page
        self.max_per_page = MAX_OPTIONS
        self.total_pages = (len(self.condicoes) - 1) // self.max_per_page + 1
        self.update_view()

    def update_view(self):
        self.clear_items()

        start = self.page * self.max_per_page
        end = start + self.max_per_page
        condicoes_pagina = self.condicoes[start:end]

        self.add_item(CondicaoSelect(condicoes_pagina, self.condicoes, self.user, offset=start))

        if self.total_pages > 1:
            if self.page > 0:
                self.add_item(PreviousPageButton())
            if self.page < self.total_pages - 1:
                self.add_item(NextPageButton())

    def get_embed_paginas(self):
        embed = Embed(
            title="📜 Condições de D&D",
            description="Lista de condições disponíveis (em ordem alfabética):",
            color=discord.Color.orange()
        )

        start = self.page * self.max_per_page
        end = start + self.max_per_page
        condicoes_pagina = self.condicoes[start:end]

        linhas = [f"• {c['nome']}" for c in condicoes_pagina]
        embed.add_field(name="Condições", value="\n".join(linhas), inline=False)
        embed.set_footer(text=f"Página {self.page + 1}/{self.total_pages}")
        return embed


# ===== BOTÕES DE PAGINAÇÃO =====
class PreviousPageButton(Button):
    def __init__(self):
        super().__init__(label="⏮️ Anterior", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: Interaction):
        view: CondicoesView = self.view
        if view.page > 0:
            view.page -= 1
            view.update_view()
            await interaction.response.edit_message(
                embed=view.get_embed_paginas(),
                view=view
            )


class NextPageButton(Button):
    def __init__(self):
        super().__init__(label="⏭️ Próximo", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: Interaction):
        view: CondicoesView = self.view
        if view.page < view.total_pages - 1:
            view.page += 1
            view.update_view()
            await interaction.response.edit_message(
                embed=view.get_embed_paginas(),
                view=view
            )

# ===== COMANDO PRINCIPAL =====
@app_commands.command(name="condicoes-dnd", description="Veja a lista de condições de D&D e detalhes de cada uma.")
@app_commands.describe(nome="Nome ou parte do nome da condição (opcional)")
async def condicoes_dnd(interaction: Interaction, nome: str = None):
    condicoes_filtradas = condicoes

    if nome:
        nome = remover_acentos(nome.lower())
        condicoes_filtradas = [
            c for c in condicoes
            if remover_acentos(c["nome"].lower()).find(nome) != -1
        ]

    if not condicoes_filtradas:
        await interaction.response.send_message("❌ Nenhuma condição encontrada com esse nome.", ephemeral=True)
        return

    view = CondicoesView(condicoes_filtradas, interaction.user)
    await interaction.response.send_message(
        embed=view.get_embed_paginas(),
        view=view,
        ephemeral=True
    )


# ===== AUTOCOMPLETE DO NOME =====
@condicoes_dnd.autocomplete("nome")
async def autocomplete_nome(interaction: Interaction, current: str):
    current = remover_acentos(current.lower())
    nomes = [
        c["nome"] for c in condicoes
        if current in remover_acentos(c["nome"].lower())
    ][:25]
    return [app_commands.Choice(name=nome, value=nome) for nome in nomes]


# ===== SETUP DO COMANDO =====
async def setup(bot):
    print("📘 Comando Condições carregado!")
    bot.tree.add_command(condicoes_dnd)
