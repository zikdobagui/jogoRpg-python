import random
import time
import os
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Item:
    nome: str
    dano: int
    defesa: int

@dataclass
class Inimigo:
    nome: str
    vida: int
    dano: int
    xp: int

class Jogador:
    def __init__(self, nome: str):
        self.nome = nome
        self.nivel = 1
        self.vida_maxima = 100
        self.vida = self.vida_maxima
        self.dano_base = 10
        self.defesa_base = 5
        self.xp = 0
        self.xp_para_nivel = 100
        self.inventario: List[Item] = []
        self.ouro = 0

    def adicionar_item(self, item: Item):
        self.inventario.append(item)

    def get_status(self):
        dano_total = self.dano_base + sum(item.dano for item in self.inventario)
        defesa_total = self.defesa_base + sum(item.defesa for item in self.inventario)
        return dano_total, defesa_total

    def subir_nivel(self):
        self.nivel += 1
        self.vida_maxima += 20
        self.vida = self.vida_maxima
        self.dano_base += 5
        self.defesa_base += 3
        self.xp_para_nivel = int(self.xp_para_nivel * 1.5)

class Jogo:
    def __init__(self):
        self.itens = {
            "Espada": Item("Espada", 15, 0),
            "Escudo": Item("Escudo", 0, 10),
            "Machado": Item("Machado", 25, -5),
            "Armadura": Item("Armadura", 0, 20)
        }
        
        self.inimigos = [
            Inimigo("Goblin", 50, 8, 30),
            Inimigo("Orc", 80, 12, 50),
            Inimigo("Troll", 120, 15, 80),
            Inimigo("Dragão", 200, 25, 150)
        ]

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def texto_lento(self, texto: str):
        for char in texto:
            print(char, end='', flush=True)
            time.sleep(0.02)
        print()

    def loja(self, jogador: Jogador):
        while True:
            self.limpar_tela()
            print(f"\nOuro: {jogador.ouro}")
            print("\nItens da Loja:")
            precos = {"Espada": 100, "Escudo": 80, "Machado": 150, "Armadura": 120}
            
            for nome_item, preco in precos.items():
                print(f"{nome_item}: {preco} ouro")
            
            escolha = input("\nO que você quer comprar? (ou 'sair'): ").title()
            
            if escolha == 'Sair':
                break
                
            if escolha in self.itens and escolha in precos:
                if jogador.ouro >= precos[escolha]:
                    jogador.adicionar_item(self.itens[escolha])
                    jogador.ouro -= precos[escolha]
                    self.texto_lento(f"\nVocê comprou {escolha}!")
                else:
                    self.texto_lento("\nOuro insuficiente!")
            else:
                self.texto_lento("\nEscolha inválida!")
            
            input("\nPressione Enter para continuar...")

    def batalha(self, jogador: Jogador, inimigo: Inimigo):
        vida_inimigo = inimigo.vida
        
        while vida_inimigo > 0 and jogador.vida > 0:
            self.limpar_tela()
            dano_jogador, defesa_jogador = jogador.get_status()
            
            print(f"\n{jogador.nome} Vida: {jogador.vida}/{jogador.vida_maxima}")
            print(f"{inimigo.nome} Vida: {vida_inimigo}/{inimigo.vida}")
            
            escolha = input("\n1. Atacar\n2. Defender\n3. Fugir\nEscolha: ")
            
            if escolha == "1":
                dano = random.randint(dano_jogador-5, dano_jogador+5)
                vida_inimigo -= dano
                self.texto_lento(f"\nVocê causou {dano} de dano ao {inimigo.nome}!")
                
            elif escolha == "2":
                defesa_jogador *= 1.5
                self.texto_lento("\nVocê assumiu uma postura defensiva!")
                
            elif escolha == "3":
                if random.random() < 0.5:
                    self.texto_lento("\nVocê conseguiu fugir!")
                    return False
                else:
                    self.texto_lento("\nNão conseguiu escapar!")
            
            if vida_inimigo > 0:
                dano = max(0, inimigo.dano - int(defesa_jogador))
                jogador.vida -= dano
                self.texto_lento(f"\n{inimigo.nome} causou {dano} de dano em você!")
                
            input("\nPressione Enter para continuar...")
        
        if jogador.vida <= 0:
            return False
        return True

    def jogar(self):
        self.limpar_tela()
        self.texto_lento("Bem-vindo à Aventura Python!")
        nome_jogador = input("\nDigite seu nome: ")
        jogador = Jogador(nome_jogador)
        
        while jogador.vida > 0:
            self.limpar_tela()
            print(f"\nNível: {jogador.nivel} | XP: {jogador.xp}/{jogador.xp_para_nivel}")
            print(f"Vida: {jogador.vida}/{jogador.vida_maxima}")
            print(f"Ouro: {jogador.ouro}")
            
            escolha = input("\n1. Lutar\n2. Loja\n3. Ver Inventário\n4. Sair\nEscolha: ")
            
            if escolha == "1":
                inimigo = random.choice(self.inimigos)
                self.texto_lento(f"\nUm {inimigo.nome} apareceu!")
                time.sleep(1)
                
                vitoria = self.batalha(jogador, inimigo)
                
                if vitoria:
                    ouro_ganho = random.randint(10, 50)
                    jogador.xp += inimigo.xp
                    jogador.ouro += ouro_ganho
                    self.texto_lento(f"\nVitória! Você ganhou {inimigo.xp} XP e {ouro_ganho} ouro!")
                    
                    if jogador.xp >= jogador.xp_para_nivel:
                        jogador.subir_nivel()
                        self.texto_lento(f"\nSubiu de Nível! Você agora é nível {jogador.nivel}!")
                else:
                    if jogador.vida <= 0:
                        self.texto_lento("\nFim de Jogo!")
                        break
            
            elif escolha == "2":
                self.loja(jogador)
            
            elif escolha == "3":
                self.limpar_tela()
                if jogador.inventario:
                    print("\nInventário:")
                    for item in jogador.inventario:
                        print(f"{item.nome} - Dano: {item.dano}, Defesa: {item.defesa}")
                else:
                    print("\nInventário está vazio!")
                input("\nPressione Enter para continuar...")
            
            elif escolha == "4":
                self.texto_lento("\nObrigado por jogar!")
                break
            
            if jogador.vida <= 0:
                self.texto_lento("\nFim de Jogo!")
                break

if __name__ == "__main__":
    jogo = Jogo()
    jogo.jogar()