import pygame

pygame.init()

# janela
tam = larg, alt = 480, 270
tela = pygame.display.set_mode(tam)

icon = pygame.image.load("player.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Shooter shooter")

# ship
class Ship:
    def __init__(self, imagem):
        self.imagem = pygame.image.load(imagem)
        self.area = self.imagem.get_rect()
        self.area.move_ip(400, 200)
        self.speed = 2

    def move(self):
        self.area = self.area.move(0, self.speed)
        if self.area.top < 0 or self.area.bottom > alt:
            self.speed = -self.speed

    def update(self, screen):
        screen.blit(self.imagem, self.area)

s = Ship("player.png")

sair = False

while not sair:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sair = True

    s.move()

    tela.fill((0, 0, 0))
    s.update(tela)
    pygame.display.flip()
    pygame.time.delay(40)

pygame.quit()
