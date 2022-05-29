import pygame
from models import Background, Text, Player, Enemy
from utils import partitions, load_sprite

class GameArea:
        def __init__(self):
                self._init_pygame()
                self.screen = pygame.display.set_mode((480, 300))
                pygame.display.set_icon(load_sprite("player", False))
                self.clock = pygame.time.Clock()
                self.active_scene = Title()
                self.record = 0

        def main_loop(self):
                while True:
                        self._handle_input()
                        self._process_game_logic()
                        self._draw()
                        self.active_scene = self.active_scene.next

        def _init_pygame(self):
                pygame.init()
                pygame.display.set_caption("Space shooter")

        def _handle_input(self):
                for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                                quit()
                                
                pressed_keys = pygame.key.get_pressed()
                
                self.active_scene.processInput(pressed_keys)

        def _process_game_logic(self):
                self.active_scene.update(self.screen)

        def _draw(self):
                self.active_scene.draw(self.screen)
                
                pygame.display.flip()
                self.clock.tick(60)

class Scene:
        def __init__(self):
                self.next = self

        def processInput(self, events, pressed_keys):
                pass

        def update(self, screen):
                for game_object in self._get_game_objects():
                                game_object.move(screen)

        def draw(self, screen):
                for game_object in self._get_game_objects():
                                game_object.draw(screen)

        def switchToScene(self, next_scene):
                self.next = next_scene

        def _get_game_objects(self):
                return []

class Title(Scene):
        def __init__(self):
                super().__init__()
                self.texts = [Text((120, 90), "Space Shooter", 50, (0, 0, 0)), Text((180, 200), "Enter space", 25, (153, 153, 0))]

        def processInput(self, pressed_keys):
                if pressed_keys[pygame.K_SPACE]:
                        self.switchToScene(Game(1))
        
        def draw(self, screen):
                screen.fill((255, 255, 255))
                super().draw(screen)

        def _get_game_objects(self):
                return [*self.texts]

class Game(Scene):
        def __init__(self, level):
                super().__init__()
                self.level = level
                self.background = Background('space', 0)
                self.bullets = []
                self.explosions = []
                self.stages = partitions(level)
                self.stage = 0
                self.enemies = []
                self.player = Player((50, 100), self.bullets.append)
                self.texts = [Text((240, 5), str(self.player.health), 20, (255, 255, 255))]

        def processInput(self, pressed_keys):
                if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
                        self.player.accelerate(-1)
                elif pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
                        self.player.accelerate(1)
                else:
                        self.player.accelerate(0)
                if pressed_keys[pygame.K_SPACE]:
                        self.player.shoot()
                if pressed_keys[pygame.K_p]:
                        self.switchToScene(Record(self.level))

        def update(self, screen):
                super().update(screen)
        
                for enemy in self.enemies:
                        if enemy.rect.centery > self.player.rect.top and enemy.rect.centery < self.player.rect.bottom:
                                enemy.shoot()

                for bullet in self.bullets[:]:
                        if bullet.rect.colliderect(self.player.rect) and bullet.classe == 'Enemy':
                                self.player.hit(bullet.damage)
                                bullet.explode(self.explosions.append)
                                self.bullets.remove(bullet)
                                break

                if self.player.health < 1:
                        self.switchToScene(Record(self.level))

                for enemy in self.enemies:
                        for bullet in self.bullets[:]:
                                if bullet.rect.colliderect(enemy.rect) and bullet.classe == 'Player':
                                        enemy.hit(bullet.damage)
                                        bullet.explode(self.explosions.append)
                                        self.bullets.remove(bullet)
                                        break

                for enemy in self.enemies[:]:
                        if enemy.health < 1:
                                self.enemies.remove(enemy)

                for bullet in self.bullets[:]:
                        if not screen.get_rect().colliderect(bullet.rect):
                                self.bullets.remove(bullet)

                self.background.move()

                if not self.enemies:
                        if self.stage < len(self.stages):
                                self.enemies = [Enemy((400, i*50+25), self.stages[self.stage][i]-1, self.bullets.append) for i in range(len(self.stages[self.stage]))]
                                self.stage += 1
                        else:
                                self.switchToScene(Game(self.level+1))

        def draw(self, screen):
                screen.fill((0, 0, 0))
                self.background.draw(screen)
                self.texts[0].update(str(self.player.health))
                super().draw(screen)
        
        def _get_game_objects(self):
                return [*self.bullets, *self.explosions, *self.enemies, *self.texts, self.player]

class Record(Scene):
        def __init__(self, record):
                super().__init__()
                self.texts = [Text((140, 90), "Game Over", 50, (255, 0, 0)), Text((160, 130), f"record: {record}", 37, (0, 0, 0)), Text((200, 200), "push P", 25, (153, 153, 0))]

        def processInput(self, pressed_keys):
                if pressed_keys[pygame.K_p]:
                        self.switchToScene(Title())

        def draw(self, screen):
                screen.fill((255, 255, 0))
                super().draw(screen)

        def _get_game_objects(self):
                return [*self.texts]
