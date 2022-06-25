from calendar import c, monthcalendar
from numpy import diagonal
import pygame 
from pygame.locals import *
from sys import exit
import os #importar pastas
from random import randrange
import variaveis


#exportando as pastas

pasta_principal = os.path.dirname(__file__)
pasta_imagens = os.path.join(pasta_principal, 'imagens') 
pasta_sons = os.path.join(pasta_principal, 'sons' ) 

pygame.init()
pygame.mixer.init()


#configuração da musica de fundo 

musica = pygame.mixer.music.load(os.path.join(pasta_sons,variaveis.musica_fundo))
pygame.mixer.music.play(-1)

#configuração da tela

tela = pygame.display.set_mode((variaveis.largura, variaveis.altura))
pygame.display.set_caption(variaveis.nome_do_jogo)

#carregando a imagem da sprite
sprite_sheet = pygame.image.load(os.path.join(pasta_imagens, 'pacman_sprite.png')).convert_alpha()#alpha conserva  a transparencia da imagem 

#criando o pacman
class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_pacman = [] # lista de sprite do pacman 
        for i in range(3): 
            img = sprite_sheet.subsurface((i * 32,0), (32,32)) 
            img = pygame.transform.scale(img, (32*3,32*3)) 
            self.imagens_pacman.append(img)  

        self.index_lista = 0 
        self.image = self.imagens_pacman[self.index_lista]
        self.rect = self.image.get_rect() 
        self.mask = pygame.mask.from_surface(self.image)
        self.y_inicial = variaveis.altura - 60 - 96//2 
        self.rect.center = (100,variaveis.altura - 60)
        self.pulo = False 
    

    #metodo pular 
    def pular(self):
        self.pulo = True 

    #metodo de atualização do pacman
    def update(self):
        if self.pulo == True:
            if self.rect.y <= 200: 
                self.pulo = False 
            self.rect.y -= 20 
        else: 
            if self.rect.y < self.y_inicial: 
                self.rect.y +=20
            else:
                self.rect.y = self.y_inicial 

        if self.index_lista > 2: 
            self.index_lista = 0
        self.index_lista += 0.25 
        self.image = self.imagens_pacman[int(self.index_lista)]

    
    
#criando as moedas
class Moedas(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((12 * 32, 0 ), (32,32)) 
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.mask = pygame.mask.from_surface(self.image) 
        self.rect = self.image.get_rect()
        self.rect.center  = (variaveis.largura, variaveis.altura-60)
        
  #fazer a moeda reiniciar na tela
    def update(self): 
        if self.rect.topright[0] < 0 :  
            self.rect.x = variaveis.largura 
        self.rect.x -= 7 


#inimigo vermelho 

class Inimigo_vermelho:
    def __init__(self):
         pygame.sprite.Sprite.__init__(self)

#inimigo rosa
class Inimigo_rosa:
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)



#inimigo amarelo 
class Inimigo_amarelo:
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

#inimigo azul 

class Inimigo_azul:
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


# gerando o piso do jogo 
class Piso(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((11 * 32, 0 ), (32,32)) 
        self.image = pygame.transform.scale(self.image, (32*4, 32*4))
        self.rect = self.image.get_rect()
        self.rect.y = variaveis.altura - 128
        self.rect.x = pos_x * 128 
    
    def update(self):
        if self.rect.topright[0] < 0 :
            self.rect.x = variaveis.largura
        self.rect.x -= 7


#adcioando o pacman 
grupo_imagens =  pygame.sprite.Group() 
pacman = Pacman() 
grupo_imagens.add(pacman)

#gerando moedas 
moeda = Moedas()
grupo_imagens.add(moeda)

grupo_moeda = pygame.sprite.Group()
grupo_moeda.add(moeda)

#gerando o piso e quantos pisos cabem na tela
for i in range(variaveis.largura*2//64):
    piso = Piso(i)
    grupo_imagens.add(piso) 

#fps do jogo
relogio = pygame.time.Clock() 

#loop principal do jogo 
while True:
    relogio.tick(variaveis.fps) 
    tela.fill(variaveis.preto)
    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            exit()
        if evento.type == KEYDOWN:
            if evento.key == K_SPACE:
                if pacman.rect.y != pacman.y_inicial: 
                    pass
                else:
                    pacman.pular()


    colisão_moeda = pygame.sprite.spritecollide(pacman, grupo_moeda, True, pygame.sprite.collide_mask)

    #adcionar sprite na tela
    grupo_imagens.draw(tela)
    
    #ficar atualizando as sprite
    grupo_imagens.update() 
    
    #atualizar a tela
    pygame.display.flip() 
