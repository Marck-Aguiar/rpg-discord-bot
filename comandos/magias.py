import discord
from discord import app_commands, Interaction, Embed
from discord.ui import Select, View, Button
import unicodedata
from utils.magias_data import magias

MAX_OPTIONS = 25

CLASSES_DISPONIVEIS = sorted(set(classe for magia in magias for classe in magia["classes"]))
ESCOLAS_DISPONIVEIS = sorted(set(magia["escola"] for magia in magias))


def remover_acentos(texto):
    return unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('ascii')


# ===== SELECT DE MAGIA =====
class MagiaSelect(Select):
    def __init__(self, magias_pagina, magias_total, user, offset=0):
        options = [
            discord.SelectOption(
                label=f"{magia['nome']} (Nível {magia['nivel']})",
                value=str(i + offset)
            )
            for i, magia in enumerate(magias_pagina)
        ][:MAX_OPTIONS]

        super().__init__(placeholder="Escolha uma magia para ver a descrição", options=options)
        self.magias_total = magias_total
        self.user = user

    async def callback(self, interaction: Interaction):
        magia_index = int(self.values[0])
        magia = self.magias_total[magia_index]

        embed = Embed(
            title=magia["nome"],
            color=discord.Color.purple()
        )
        embed.add_field(name="Nível", value=str(magia["nivel"]), inline=True)
        embed.add_field(name="Escola", value=magia["escola"], inline=True)
        embed.add_field(name="Tempo de Conjuração", value=magia["tempo_conjuracao"], inline=True)
        embed.add_field(name="Alcance", value=magia["alcance"], inline=True)
        embed.add_field(name="Componentes", value=magia["componentes"], inline=True)
        embed.add_field(name="Duração", value=magia["duracao"], inline=True)
        embed.add_field(name="Descrição", value=magia["descricao"], inline=False)

        await interaction.channel.send(
            f"{self.user.mention} escolheu a magia **{magia['nome']}**! Confira as informações abaixo:",
            embed=embed
        )
        await interaction.response.defer()


# ===== BOTÕES DE PAGINAÇÃO =====
class PreviousPageButton(Button):
    def __init__(self):
        super().__init__(label="⏮️ Anterior", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: Interaction):
        view: MagiaView = self.view
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
        view: MagiaView = self.view
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
class MagiaView(View):
    def __init__(self, magias, user, classe, nivel=None, nome=None, escola=None, page=0):
        super().__init__(timeout=None)
        self.magias = sorted(magias, key=lambda m: (m["nivel"], remover_acentos(m["nome"])))
        self.user = user
        self.classe = classe
        self.nivel = nivel
        self.nome = nome
        self.escola = escola
        self.max_per_page = MAX_OPTIONS
        self.page = page
        self.total_pages = (len(self.magias) - 1) // self.max_per_page + 1
        self.message_text = ""
        self.update_view()

    def update_view(self):
        self.clear_items()

        start = self.page * self.max_per_page
        end = start + self.max_per_page
        magias_pagina = self.magias[start:end]

        self.add_item(MagiaSelect(magias_pagina, self.magias, self.user, offset=start))

        if self.total_pages > 1:
            if self.page > 0:
                self.add_item(PreviousPageButton())
            if self.page < self.total_pages - 1:
                self.add_item(NextPageButton())

        self.add_item(CloseButton())

        self.message_text = "🔎 Selecione uma magia para ver os detalhes:"

    def get_embed_paginas(self):
        titulo = f"📚 Magias da classe {self.classe}" if self.classe else "📚 Todas as Magias"
        if self.nivel is not None:
            titulo += f" - Nível {self.nivel}"
        if self.nome:
            titulo = f"📚 Resultados para '{self.nome}'"
        if self.escola:
            titulo += f" - Escola {self.escola}"

        embed = Embed(
            title=titulo,
            description="Listagem por nível (em ordem alfabética):",
            color=discord.Color.dark_purple()
        )

        start = self.page * self.max_per_page
        end = start + self.max_per_page
        magias_pagina = self.magias[start:end]

        magias_por_nivel = {}
        for magia in magias_pagina:
            magias_por_nivel.setdefault(magia["nivel"], []).append(magia)

        for nivel in sorted(magias_por_nivel.keys()):
            lista_nivel = sorted(magias_por_nivel[nivel], key=lambda m: remover_acentos(m["nome"]))
            nomes = "\n".join(f"• {m['nome']}" for m in lista_nivel)
            embed.add_field(name=f"Nível {nivel}", value=nomes[:1024], inline=False)

        embed.set_footer(text=f"Página {self.page + 1}/{self.total_pages}")
        return embed


# ===== COMANDO PRINCIPAL =====
@app_commands.command(name="magia", description="Buscar magias por classe, nível, nome ou escola.")
@app_commands.describe(classe="Classe que pode conjurar a magia", nivel="(Opcional) Nível da magia", nome="(Opcional) Nome da magia", escola="(Opcional) Escola de magia")
async def magia(interaction: Interaction, classe: str = None, nivel: int = None, nome: str = None, escola: str = None):
    if nome:
        nome = remover_acentos(nome.lower())
        magias_encontradas = [
            magia for magia in magias
            if remover_acentos(magia["nome"].lower()).find(nome) != -1
        ]
        if not magias_encontradas:
            await interaction.response.send_message(f"⚠️ Nenhuma magia com o nome '{nome}' foi encontrada.", ephemeral=True)
            return
        view = MagiaView(magias_encontradas, interaction.user, classe="", nome=nome)
        await interaction.response.send_message(
            embed=view.get_embed_paginas(),
            content="🔎 Resultados da busca por nome:",
            view=view
        )
        return

    # Filtragem por escola
    if escola:
        escola = escola.capitalize()
        magias_escola = [m for m in magias if m["escola"] == escola]
        if not magias_escola:
            await interaction.response.send_message(f"Nenhuma magia encontrada para a escola {escola}.", ephemeral=True)
            return
        magias_filtradas = magias_escola
    else:
        magias_filtradas = magias

    if classe:  # Se a classe for fornecida, a busca será feita para essa classe.
        classe = classe.capitalize()
        magias_classe = [m for m in magias_filtradas if classe in m["classes"]]
        if not magias_classe:
            await interaction.response.send_message(f"Nenhuma magia encontrada para a classe {classe}.", ephemeral=True)
            return

        magias_filtradas = [m for m in magias_classe if m["nivel"] == nivel] if nivel is not None else magias_classe
        if not magias_filtradas:
            await interaction.response.send_message(f"Nenhuma magia de nível {nivel} para {classe}.", ephemeral=True)
            return

    view = MagiaView(magias_filtradas, interaction.user, classe=classe, nivel=nivel, escola=escola)
    await interaction.response.send_message(
        embed=view.get_embed_paginas(),
        content=view.message_text,
        view=view
    )


# ===== AUTOCOMPLETE DE CLASSE =====
@magia.autocomplete("classe")
async def autocomplete_classe(interaction: Interaction, current: str):
    current = current.lower()
    return [
        app_commands.Choice(name=classe, value=classe)
        for classe in CLASSES_DISPONIVEIS
        if current in classe.lower()
    ][:25]


# ===== AUTOCOMPLETE DE NÍVEL =====
@magia.autocomplete("nivel")
async def autocomplete_nivel(interaction: Interaction, current: str):
    classe_escolhida = interaction.namespace.classe
    if not classe_escolhida:
        return []

    classe_escolhida = classe_escolhida.capitalize()

    niveis_disponiveis = sorted(
        set(magia["nivel"] for magia in magias if classe_escolhida in magia["classes"])
    )

    try:
        current_int = int(current)
        niveis_sugeridos = [n for n in niveis_disponiveis if str(n).startswith(str(current_int))]
    except ValueError:
        niveis_sugeridos = niveis_disponiveis

    return [
        app_commands.Choice(name=f"Nível {nivel}", value=nivel)
        for nivel in niveis_sugeridos[:25]
    ]


# ===== AUTOCOMPLETE DE NOME DE MAGIA =====
@magia.autocomplete("nome")
async def autocomplete_magia_nome(interaction: Interaction, current: str):
    current_normalizado = remover_acentos(current.lower())
    nomes_encontrados = [
        magia["nome"]
        for magia in magias
        if remover_acentos(magia["nome"].lower()).startswith(current_normalizado)
    ]

    return [
        app_commands.Choice(name=nome, value=nome)
        for nome in nomes_encontrados[:25]
    ]


# ===== AUTOCOMPLETE DE ESCOLA =====
@magia.autocomplete("escola")
async def autocomplete_escola(interaction: Interaction, current: str):
    current = current.lower()
    return [
        app_commands.Choice(name=escola, value=escola)
        for escola in ESCOLAS_DISPONIVEIS
        if current in escola.lower()
    ][:25]


# ===== SETUP DO COMANDO =====
async def setup(bot):
    print("✨ Comando Magias carregado!")
    bot.tree.add_command(magia)
