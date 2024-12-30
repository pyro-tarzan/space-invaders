from turtle import Turtle, Screen
import time


class SpaceInvaders:
    def __init__(self):
        self.screen = Screen()
        self.ship = Turtle("square")
        self.enemies = Overlay()
        self.bullet = Bullet()
        self.title = Turtle()
        self.controls = Turtle()
        self.initial = self.setup_gui()
        self.enemy_count = len(self.enemies.enemies)

    def setup_gui(self):
        # SETUP SCREEN
        self.screen.title("Space - Invaders")
        self.screen.bgcolor("black")
        self.screen.screensize(400, 400)

        # SETUP SHAPE, SIZE AND POS
        self.screen.tracer(0)

        self.title.penup()
        self.title.hideturtle()
        self.title.color("white")
        self.title.setposition(0, 370)
        self.title.write("Space Invaders", align="center", font=("Arial", 20, "normal"))

        self.controls.penup()
        self.controls.hideturtle()
        self.controls.color("white")
        self.controls.setposition(0, 340)
        self.controls.write("Move Left - 'a' & Move Right - 'd'", align="center", font=("Arial", 18, "normal"))

        self.ship.color("white")
        self.ship.shapesize(stretch_len=3, stretch_wid=1)
        self.ship.penup()
        self.ship.setposition(0, -310)
        self.enemies.create_enemies()
        self.screen.update()

    def move_left(self):
        if self.ship.xcor() >= -400:
            self.ship.goto(self.ship.xcor() - 20, self.ship.ycor())
    
    def move_right(self):
        if self.ship.xcor() <= 400:
            self.ship.goto(self.ship.xcor() + 20, self.ship.ycor())
        
    def fire_bullet(self):
        if not self.bullet.isvisible():
            self.bullet.showturtle()

    def update_bullet(self):
        if self.bullet.isvisible() and self.bullet.ycor() < 400:
            self.bullet.goto(self.bullet.xcor(), self.bullet.ycor() + 30)
        else:
            self.bullet.hideturtle()
            self.bullet.setposition(self.ship.xcor(), self.ship.ycor())
        
    def check_collision(self):
        for enemy in self.enemies.enemies:
            if self.bullet.isvisible() and enemy.isvisible():
                if self.bullet.distance(enemy) < 15:
                    self.bullet.hideturtle()
                    enemy.hideturtle()
                    self.enemy_count -=1
                    break


    def run(self):
        self.screen.listen()
        self.screen.onkey(self.move_left, "a")
        self.screen.onkey(self.move_right, "d")
        self.screen.onkey(self.fire_bullet, "space")

        while True:
            if self.enemy_count > 0:
                time.sleep(.1)
                self.enemies.move_overlay()
                self.update_bullet()
                self.check_collision()
                self.screen.update()
            else:
                break
            
        self.gameover = Turtle()
        self.gameover.penup()
        self.gameover.hideturtle()
        self.gameover.color("white")
        self.gameover.write("Game Over.", align="center", font=("Arial", 30, "normal"))
        self.screen.mainloop()


class Enemy(Turtle):
    def __init__(self, xpos: int, ypos:int):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.penup()
        self.goto(xpos, ypos)


class Bullet(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.shapesize(.2, .2)
        self.penup()
        self.hideturtle()


class Overlay:
    def __init__(self):
        self.enemies = []
        self.positions = [-200, 300]
        self.moving_right = True

    def create_enemies(self):
        self.relative_postion = []
        gap_x, gap_y = 30, 50
        for row in range(3):
            for col in range(10):
                x_pos = col * gap_y
                y_pos = -row * gap_x
                self.relative_postion.append((x_pos, y_pos))
                enemy = Enemy(self.positions[0] + x_pos,self.positions[1] + y_pos)
                self.enemies.append(enemy)
    
    def move_overlay(self):
        step = 10 if self.moving_right else -10
        self.positions[0] += step

        left_edge = self.positions[0]
        right_edge = self.positions[0] + 10 * 40

        if right_edge > 400 or left_edge < -400:
            self.moving_right = not self.moving_right
        
        self.update_enemy_positions()

    def update_enemy_positions(self):
        for i, enemy in enumerate(self.enemies):
            if enemy.isvisible():
                x, y = self.relative_postion[i]
                enemy.goto(self.positions[0] + x, self.positions[1] + y)