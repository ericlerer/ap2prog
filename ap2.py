import random

def aventura_andar(aventureiro, direcao):
    movimento = direcao.upper()
    if movimento == "W" and aventureiro["posicao"][1] > 0:
        aventureiro["posicao"][1] -= 1
        return True
    elif movimento == "A" and aventureiro["posicao"][0] > 0:
        aventureiro["posicao"][0] -= 1
        return True
    elif movimento == "S" and aventureiro["posicao"][1] < 9:
        aventureiro["posicao"][1] += 1
        return True
    elif movimento == "D" and aventureiro["posicao"][0] < 9:
        aventureiro["posicao"][0] += 1
        return True
    return False

def aventura_atacar(aventureiro):
    return aventureiro["forca"] + random.randint(1, 6)

def aventura_defender(aventureiro, dano):
    dano_recebido = max(dano - aventureiro["defesa"], 0)
    aventureiro["vida"] -= dano_recebido
    aventureiro["vida"] = max(aventureiro["vida"], 0)

def ver_atributos_aventureiro(aventureiro):
    print(f"Atributos do {aventureiro['nome']}:")
    print(f"Nível: {aventureiro['nivel']}")
    print(f"Experiência: {aventureiro['experiencia']} / {aventureiro['exp_para_nivel']}")
    print(f"Vida: {aventureiro['vida']} / {aventureiro['vida_maxima']}")
    print(f"Força: {aventureiro['forca']}")
    print(f"Defesa: {aventureiro['defesa']}")

def aventura_esta_vivo(aventureiro):
    return aventureiro["vida"] > 0

def novo_monstro():
    print("Um novo monstro apareceu!")
    return {
        "forca": random.randint(5, 25),
        "vida": random.randint(10, 100)
    }

def monstro_atacar(monstro):
    return random.randint(5, 25)

def monstro_defender(monstro, dano):
    monstro["vida"] -= dano

def monstro_esta_vivo(monstro):
    return monstro["vida"] > 0

def desenhar(aventureiro, tesouro, pocao, rodadas):
    for y in range(10):
        for x in range(10):
            if [x, y] == aventureiro["posicao"]:
                print("@", end=" ")
            elif [x, y] == tesouro:
                print("\033[91mX\033[0m", end=" ")  # Tesouro em vermelho
            elif [x, y] == pocao:
                print("%", end=" ")
            else:
                print(".", end=" ")
        print()
    # Centralizar a mensagem
    print(f"\nRodadas: {rodadas}".center(40))
    print(f"Aventureiro nv {aventureiro['nivel']} ({aventureiro['experiencia']} / {aventureiro['exp_para_nivel']}) - "
          f"Vida {aventureiro['vida']} / {aventureiro['vida_maxima']} - Força {aventureiro['forca']} - Defesa {aventureiro['defesa']}".center(40))

def iniciar_combate(aventureiro, monstro):
    while True:
        dano_aventureiro = aventura_atacar(aventureiro)
        monstro_defender(monstro, dano_aventureiro)
        print(f"Você causou {dano_aventureiro} de dano ao monstro!")
        print(f"Vida atual do monstro: {monstro['vida']}")
        if not monstro_esta_vivo(monstro):
            print("Você derrotou o monstro!")
            ganhar_experiencia(aventureiro, 5)
            return True

        dano_monstro = monstro_atacar(monstro)
        aventura_defender(aventureiro, dano_monstro)
        print(f"O monstro causou {dano_monstro} de dano a você!")
        print(f"Sua vida atual: {aventureiro['vida']}")
        if not aventura_esta_vivo(aventureiro):
            print("Você foi derrotado pelo monstro...")
            return False

def movimentar(aventureiro, direcao, pocao):
    if not aventura_andar(aventureiro, direcao):
        return True

    if aventureiro["posicao"] == pocao:
        aplicar_efeito_pocao(aventureiro)
        pocao.clear()

    efeito = random.choices(["nada", "monstro"], [0.6, 0.4])[0]
    if efeito == "monstro":
        monstro = novo_monstro()
        return iniciar_combate(aventureiro, monstro)

    return True

def aplicar_efeito_pocao(aventureiro):
    efeito = random.choice(["vida", "forca", "defesa"])
    if efeito == "vida":
        aventureiro["vida_maxima"] *= 2
        aventureiro["vida"] = aventureiro["vida_maxima"]
        print("A poção dobrou sua vida máxima e recuperou toda a sua vida!")
    elif efeito == "forca":
        aventureiro["forca"] += 15
        print("A poção aumentou sua força em 15!")
    elif efeito == "defesa":
        aventureiro["defesa"] += 10
        print("A poção aumentou sua defesa em 10!")

def gerar_tesouro():
    tesouro = [random.randint(1, 9), random.randint(1, 9)]
    while tesouro == [0, 0]:
        tesouro = [random.randint(1, 9), random.randint(1, 9)]
    return tesouro

def gerar_pocao():
    pocao = [random.randint(1, 9), random.randint(1, 9)]
    while pocao == [0, 0]:
        pocao = [random.randint(1, 9), random.randint(1, 9)]
    return pocao

def ganhar_experiencia(aventureiro, quantidade):
    aventureiro["experiencia"] += quantidade
    if aventureiro["experiencia"] >= aventureiro["exp_para_nivel"]:
        aventureiro["experiencia"] -= aventureiro["exp_para_nivel"]
        aventureiro["nivel"] += 1
        aventureiro["exp_para_nivel"] = int(aventureiro["exp_para_nivel"] * 1.5)
        aventureiro["vida_maxima"] += 20
        aventureiro["vida"] = aventureiro["vida_maxima"]
        aventureiro["forca"] += 2
        aventureiro["defesa"] += 2
        print(f"Parabéns! Você subiu para o nível {aventureiro['nivel']}!")

def main():
    aventureiro = {
        "forca": random.randint(10, 18),
        "defesa": random.randint(10, 18),
        "vida": random.randint(100, 120),
        "vida_maxima": random.randint(100, 120),
        "posicao": [0, 0],
        "nivel": 1,
        "experiencia": 0,
        "exp_para_nivel": 5
    }

    tesouro = gerar_tesouro()
    pocao = gerar_pocao()
    rodadas = 0

    aventureiro["nome"] = input("Deseja buscar um tesouro? Primeiro, informe seu nome: ")
    print(f"Saudações, {aventureiro['nome']}! Boa sorte!")

    desenhar(aventureiro, tesouro, pocao, rodadas)

    while True:
        op = input("Insira o seu comando: ").upper()
        if op == "Q":
            print("Já correndo?")
            break
        elif op == "T":
            ver_atributos_aventureiro(aventureiro)
        elif op in ["W", "A", "S", "D"]:
            if movimentar(aventureiro, op, pocao):
                rodadas += 1
                desenhar(aventureiro, tesouro, pocao, rodadas)
            else:
                print("Game Over...")
                break
        else:
            print(f"{aventureiro['nome']}, não conheço essa opção! Tente novamente!")

        if aventureiro["posicao"] == tesouro:
            print(f"Parabéns, {aventureiro['nome']}! Você encontrou o tesouro!")
            break

if __name__ == "__main__":
    main()
