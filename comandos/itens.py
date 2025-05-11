import discord
from discord import app_commands, Interaction, Embed
from discord.ui import Select, View, Button
import unicodedata
from utils.itens_data import itens

MAX_OPTIONS = 25
TIPOS_ITENS = sorted(itens.keys())

def remover_acentos(texto):
    return unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('ascii')


# ===== SELECT DE ITEM =====
class ItemSelect(Select):
    def __init__(self, itens_pagina, itens_total, user, offset=0):
        options = []

        for i, item in enumerate(itens_pagina):
            nome = item["nome"]
            valor_extra = ""

            if "dano" in item:
                valor_extra = f" ({item['dano']})"
            elif "classe_armadura" in item:
                valor_extra = f" (CA {item['classe_armadura']})"

            label = f"{nome}{valor_extra}"

            options.append(discord.SelectOption(
                label=label[:100],
                value=str(i + offset)
            ))

        super().__init__(placeholder="Escolha um item para ver a descrição", options=options)
        self.itens_total = itens_total
        self.user = user

    async def callback(self, interaction: Interaction):
        item_index = int(self.values[0])
        item = self.itens_total[item_index]

        embed = Embed(
            title=item["nome"],
            color=discord.Color.purple()
        )

        if "classe_armadura" in item:
            embed.add_field(name="Classe de Armadura", value=str(item["classe_armadura"]), inline=True)
        if "dano" in item:
            embed.add_field(name="Dano", value=item["dano"], inline=True)
        if "peso" in item:
            embed.add_field(name="Peso", value=str(item["peso"]), inline=True)
        if "preco" in item:
            embed.add_field(name="Preço", value=str(item["preco"]), inline=True)
        if "descricao" in item:
            embed.add_field(name="Descrição", value=item["descricao"], inline=False)
        if "forca" in item:
            embed.add_field(name="Força", value=str(item["forca"]), inline=True)
        if "furtividade" in item:
            embed.add_field(name="Furtividade", value=str(item["furtividade"]), inline=True)
        if "categoria" in item:
            embed.add_field(name="Categoria", value=str(item["categoria"]), inline=True)
        if "tempo_vestir" in item:
            embed.add_field(name="Tempo para vestir", value=str(item["tempo_vestir"]), inline=True)
        if "tempo_remover" in item:
            embed.add_field(name="Tempo para remover", value=str(item["tempo_remover"]), inline=True)

        await interaction.channel.send(
            f"{self.user.mention} escolheu o item **{item['nome']}**! Confira as informações abaixo:",
            embed=embed
        )
        await interaction.response.defer()


# ===== BOTÕES DE PAGINAÇÃO =====
class PreviousPageButton(Button):
    def __init__(self):
        super().__init__(label="⏮️ Anterior", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: Interaction):
        view: ItemView = self.view
        if view.page > 0:
            view.page -= 1
            view.update_view()
            await interaction.response.edit_message(
                content=view.message_text,
                embed=view.get_embed_paginas(),
                view=view
            )


class NextPageButton(Button):
    def __init__(self):
        super().__init__(label="⏭️ Próximo", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: Interaction):
        view: ItemView = self.view
        if view.page < view.total_pages - 1:
            view.page += 1
            view.update_view()
            await interaction.response.edit_message(
                content=view.message_text,
                embed=view.get_embed_paginas(),
                view=view
            )


class CloseButton(Button):
    def __init__(self):
        super().__init__(label="🗙 Fechar", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: Interaction):
        await interaction.message.delete()


# ===== VIEW COM PAGINAÇÃO DO SELECT E EMBED =====
class ItemView(View):
    def __init__(self, itens, user, tipo, page=0):
        super().__init__(timeout=None)
        self.itens = sorted(itens, key=lambda e: remover_acentos(e["nome"]))
        self.user = user
        self.tipo = tipo
        self.max_per_page = MAX_OPTIONS
        self.page = page
        self.total_pages = (len(self.itens) - 1) // self.max_per_page + 1
        self.message_text = ""
        self.update_view()

    def update_view(self):
        self.clear_items()

        start = self.page * self.max_per_page
        end = start + self.max_per_page
        itens_pagina = self.itens[start:end]

        self.add_item(ItemSelect(itens_pagina, self.itens, self.user, offset=start))

        if self.total_pages > 1:
            if self.page > 0:
                self.add_item(PreviousPageButton())
            if self.page < self.total_pages - 1:
                self.add_item(NextPageButton())

        self.add_item(CloseButton())
        self.message_text = "🔎 Selecione um item para ver os detalhes:"

    def get_embed_paginas(self):
        titulo = f":school_satchel: Itens do tipo {self.tipo.capitalize()}"
        embed = Embed(
            title=titulo,
            description="Listagem dos itens (em ordem alfabética):",
            color=discord.Color.dark_purple()
        )

        start = self.page * self.max_per_page
        end = start + self.max_per_page
        itens_pagina = self.itens[start:end]

        linhas = []
        for item in itens_pagina:
            nome = item["nome"]
            if "dano" in item:
                nome += f" ({item['dano']})"
            elif "classe_armadura" in item:
                nome += f" (CA {item['classe_armadura']})"
            linhas.append(f"• {nome}")

        embed.add_field(name=f"{self.tipo.capitalize()}", value="\n".join(linhas)[:1024], inline=False)
        embed.set_footer(text=f"Página {self.page + 1}/{self.total_pages}")
        return embed


# ===== COMANDO PRINCIPAL =====
@app_commands.command(name="itens", description="Buscar itens por tipo, categoria e nome.")
@app_commands.describe(
    tipo="Tipo de item (armaduras, armas, ferramentas, etc.)",
    categoria="Categoria opcional (leve, corpo-a-corpo, escudo, etc.)",
    nome="Nome ou parte do nome do item (opcional)"
)
async def item(interaction: Interaction, tipo: str, categoria: str = None, nome: str = None):
    tipo = tipo.lower()

    if tipo not in itens:
        await interaction.response.send_message(f"Tipo de item '{tipo}' não encontrado.", ephemeral=True)
        return

    itens_tipo = itens[tipo]

    # Filtro por categoria
    if categoria:
        categoria = remover_acentos(categoria.lower())
        itens_tipo = [
            i for i in itens_tipo
            if 'categoria' in i and remover_acentos(i['categoria'].lower()).find(categoria) != -1
        ]

    # Filtro por nome
    if nome:
        nome = remover_acentos(nome.lower())
        itens_tipo = [
            i for i in itens_tipo
            if remover_acentos(i["nome"].lower()).find(nome) != -1
        ]

    if not itens_tipo:
        await interaction.response.send_message(
            "Nenhum item encontrado com os filtros informados.",
            ephemeral=True
        )
        return

    view = ItemView(itens_tipo, interaction.user, tipo=tipo)
    await interaction.response.send_message(
        embed=view.get_embed_paginas(),
        content=view.message_text,
        view=view
    )


# ===== AUTOCOMPLETE DE TIPO =====
@item.autocomplete("tipo")
async def autocomplete_tipo(interaction: Interaction, current: str):
    current = current.lower()
    return [
        app_commands.Choice(name=tipo, value=tipo)
        for tipo in TIPOS_ITENS
        if current in tipo
    ][:25]


# ===== AUTOCOMPLETE DE CATEGORIA =====
@item.autocomplete("categoria")
async def autocomplete_categoria(interaction: Interaction, current: str):
    tipo_atual = interaction.namespace.tipo
    current = remover_acentos(current.lower())

    if not tipo_atual or tipo_atual.lower() not in itens:
        return []

    categorias = set(
        remover_acentos(i["categoria"])
        for i in itens[tipo_atual.lower()]
        if "categoria" in i
    )

    return [
        app_commands.Choice(name=cat, value=cat)
        for cat in categorias
        if current in remover_acentos(cat.lower())
    ][:25]


# ===== SETUP DO COMANDO =====
async def setup(bot):
    print("📦 Comando Itens carregado!")
    bot.tree.add_command(item)
