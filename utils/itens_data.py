# itens_data.py

from utils.itens_pacotes import pacotes
from utils.itens_ferramentas import ferramentas
from utils.itens_equipamentos import equipamento_de_aventura
from utils.itens_armaduras import armaduras
from utils.itens_armas import armas

# Dicionário de todos os itens, classificados por tipo
itens = {
    "pacotes": pacotes,
    "ferramentas": ferramentas,
    "equipamentos": equipamento_de_aventura,
    "armaduras": armaduras,
    "armas": armas,
}
