#Fifth Project : The Snake
import pygame
import numpy as np

#Musica 
file = 'Isaac.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play(-1)

class Game(object):

#ventana
    def __init__(self, ancho_juego, alto_juego):
        pygame.display.set_caption('The binding of isnaake')
        self.ancho_juego = ancho_juego
        self.alto_juego = alto_juego
        self.display_juego = pygame.display.set_mode((ancho_juego, alto_juego+100))
        self.fondo = pygame.image.load('snake.jpg')
        self.colision = False
        self.score = 0 
        self.font = pygame.font.SysFont('Ubuntu', 20)
#resultado
    def display_ui(self, record):
        self.display_juego.fill((255, 255, 255))
        score_txt = self.font.render('RESULTADO: ', True, (0, 0, 0))
        score_num = self.font.render(str(self.score), True, (0, 0, 0))
        record_txt = self.font.render('MEJOR: ', True, (0, 0, 0))
        record_num = self.font.render(str(record), True, (0, 0, 0))

        pygame.draw.rect(self.display_juego, (200, 200, 200), (0, self.alto_juego, self.alto_juego, 100))

        self.display_juego.blit(score_txt, (30, 480))
        self.display_juego.blit(score_num, (160, 480))
        self.display_juego.blit(record_txt, (280, 480))
        self.display_juego.blit(record_num, (360, 480))
        self.display_juego.blit(self.fondo, (0, 0))

    def obtener_record(self, score, record):
        return score if score >= record else record

#objetos y serpiente

class Player(object):

    def __init__(self):
        self.x = 100
        self.y = 100
        self.posicion = []
        self.posicion.append([self.x, self.y])
        self.n_shit = 1
        self.comida = False
        self.comidados = False
        self.imagen = pygame.image.load('pixel.jpg')
        self.cambio_x = 20
        self.cambio_y = 0
        self.direccion =[1, 0]

    def refrescar_posiciones(self, x, y):
        if self.posicion[-1] [0] != x or self.posicion[-1] [0] != y:
            if self.n_shit > 1:
                for i in range(self.n_shit - 1):
                    self.posicion[i] [0], self.posicion[i] [1] = self.posicion[i + 1]

            self.posicion[-1] [0] = x
            self.posicion[-1] [1] = y

    def hacer_movimiento(self, x, y, game, food, foodtwo):
        array_m = [self.cambio_x, self.cambio_y]

        if self.comida:
            self.posicion.append([self.x, self.y])
            self.comida = False
            self.n_shit += 1

        if self.comidados:
            self.posicion.append([self.x, self.y])
            self.comidados = False
            self.n_shit += 1

#controles
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT and self.direccion != [1, 0]:
                    array_m = [-20, 0]
                    self.direccion = [-1, 0]
                elif e.key == pygame.K_RIGHT and self.direccion != [-1, 0]:
                    array_m = [20, 0]
                    self.direccion = [1, 0]
                elif e.key == pygame.K_UP and self.direccion != [0 , -1]:
                    array_m = [0, -20]
                    self.direccion = [0, 1]
                elif e.key == pygame.K_DOWN and self.direccion != [0, 1]:
                    array_m = [0, 20]
                    self.direccion = [0, -1]

        self.cambio_x, self.cambio_y = array_m
        self.x = x + self.cambio_x
        self.y = y + self.cambio_y

        if self.x < 0 or self.x > game.ancho_juego-20 \
                or self.y < 0 or self.y > game.alto_juego-20 \
                or [self.x, self.y] in self.posicion:
            game.colision = True

        food.comer(self, game)
        self.refrescar_posiciones(self.x, self.y)

        foodtwo.comer(self, game)
        self.refrescar_posiciones(self.x, self.y)

    def display_jugador(self, x, y, game):
        self.posicion[-1][0] = x
        self.posicion[-1][1] = y

        if game.colision == False:
            for i in range(self.n_shit):
                x_temp, y_temp = self.posicion[len(self.posicion) -1 -i]
                game.display_juego.blit(self.imagen, (x_temp, y_temp))

#comidas

class Food(object):

    def __init__(self):
        self.x_food = 200
        self.y_food = 200
        self.imagen = pygame.image.load('shitt.jpg')

    def comida_coor(self, game, player):
        x_rand = np.random.choice(list(range(0, game.ancho_juego, 20)))
        self.x_food = x_rand
        y_rand = np.random.choice(list(range(0, game.alto_juego, 20)))
        self.y_food = y_rand

    def display_comida(self, x, y, game):
        game.display_juego.blit(self.imagen, (x, y))

    def comer(self, player, game):
        if player.x == self.x_food and player.y == self.y_food:
            self.comida_coor(game, player)
            player.comida = True
            game.score += 1

class Foodtwo(object):

    def __init__(self):
        self.x_foodtwo = 200
        self.y_foodtwo = 300
        self.imagen = pygame.image.load('dessert.png')

    def comida_coor(self, game, player):
        x_rand = np.random.choice(list(range(0, game.ancho_juego, 20)))
        self.x_foodtwo = x_rand
        y_rand = np.random.choice(list(range(0, game.alto_juego, 20)))
        self.y_foodtwo = y_rand

    def display_comida(self, x, y, game):
        game.display_juego.blit(self.imagen, (x, y))

    def comer(self, player, game):
        if player.x == self.x_foodtwo and player.y == self.y_foodtwo:
            self.comida_coor(game, player)
            player.comidados = True
            game.score += 1



#iniciacion juego
def run():
    pygame.init()
    record = 0
    clock = pygame.time.Clock()
    while True:
        game = Game(420, 420)
        player = Player()
        food = Food()
        foodtwo = Foodtwo()

        game.display_ui(record)
        player.display_jugador(player.x, player.y, game)
        food.display_comida(food.x_food, food.y_food, game)
        foodtwo.display_comida(foodtwo.x_foodtwo, foodtwo.y_foodtwo, game)
        pygame.display.update()

        while not game.colision:
            player.hacer_movimiento(player.x, player.y, game, food, foodtwo)
            record = game.obtener_record(game.score, record)
            game.display_ui(record)
            player.display_jugador(player.x, player.y, game)
            food.display_comida(food.x_food, food.y_food, game)
            foodtwo.display_comida(foodtwo.x_foodtwo, foodtwo.y_foodtwo, game)
            pygame.display.update()
            clock.tick(10)

if __name__ == '__main__':
    run()





