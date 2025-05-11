import re
import random

def rolar_dados(comando: str):
    comando = comando.strip()
    nome = ""
    resultado_final = []

    partes = comando.split()
    if len(partes) > 1:
        comando, nome = partes[0], ' '.join(partes[1:])

    padrao = r'(?:(\d+)#)?(\d*)[dD](\d+)([+-]\d+)?'
    match = re.fullmatch(padrao, comando)
    if not match:
        return "❌ Formato inválido. Ex: 3d6, 2d20+1, 4#d8-2"

    repeticoes = int(match.group(1)) if match.group(1) else 1
    quantidade = int(match.group(2)) if match.group(2) else 1
    faces = int(match.group(3))
    modificador = int(match.group(4)) if match.group(4) else 0

    for _ in range(repeticoes):
        rolagens = [random.randint(1, faces) for _ in range(quantidade)]
        explosao = any(r == 1 or r == faces for r in rolagens)
        emoji_explosao = " 💥" if explosao else ""
        total = sum(rolagens) + modificador
        mod_str = f"{modificador:+}" if modificador != 0 else ""
        dados_str = f"{quantidade}d{faces}{mod_str}"
        resultado_final.append(f":game_die: **`{total}`**{emoji_explosao} ⟵ {rolagens} {dados_str}")

    if nome:
        return f"🎲 **{nome}**, \n" + "\n".join(resultado_final)
    else:
        return "\n".join(resultado_final)
