# Sound played using playsound module, which requires installation of Python ObjC package  -  pyobjc

import turtle
import os
import math
from playsound import playsound
import threading


class playFireSoundThread (threading.Thread):
   def __init__(self, sound):
      threading.Thread.__init__(self)
      self.sound = sound
   def run(self):
      playsound(self.sound)

#Setup the screen
window = turtle.Screen()
window.bgcolor("black")
window.title("Space Invaders")

#Register images
window.register_shape("space_invaders.gif")
window.register_shape("ship.gif")
window.register_shape("bullet.gif")

#Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.forward(600)
    border_pen.left(90)
border_pen.hideturtle()


#Explaination for String formatting
#We have been doing formatting this way:
demonstring = "I am {}".format("Kenny")
#We can replace strings with different data like this:
# %s - String
# %d - Integers
# %f - Floats
# %.<#OfDecimals>f  - Float to a number of decimal points
# Format: "Here is a string %s, my float to 2 deci: %.2f" % ("Hello World", 25.36225)

#In-Class exercise:
#Question Prompt:
# You will need to print the following sentence:
# We are A and B, We have $50 dollars. We own you $38.22 dollars! Here you go.
# Here are the sentence you need to use
# tempString = "We are %s and %s, We have $%d dollars. We own you $%.2f dollars! Here you go."
# print(tempString % ("A", "B", 50, 38.2234))



#Game Scores
score = 0

#Draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setpos(-290, -280)
scorestring = "Score: %s" % score
#If move is true, pen is then moved to the bottom right of the text
score_pen.write(scorestring, False, align = "left", font = ("Arial", 14, "normal"))
score_pen.hideturtle()

#Creating the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("ship.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

playerspeed = 15

#Enemies:
#Choose a number of enemies
number_of_enemies = 16
#Create an empty list of enemies
enemies = []

def spawn_enemies():
    # Add enemies to the list
    for i in range(number_of_enemies):
        # create the enemy
        enemies.append(turtle.Turtle())
        enemies[i].penup()
        enemies[i].shape("space_invaders.gif")
        enemies[i].speed(0)
    # Setting position - First 5 Enemies
    xPos = -100
    yPos = 250
    for i in range(5):
        enemies[i].setposition(xPos, yPos)
        xPos += 50
    # Setting position - Next 6 Enemies
    xPos = -125
    yPos = 200
    for i in range(5, 11):
        enemies[i].setposition(xPos, yPos)
        xPos += 50
    # Setting position - Final 5 Enemies
    xPos = -100
    yPos = 150
    for i in range(11, 16):
        enemies[i].setposition(xPos, yPos)
        xPos += 50




enemyspeed = 2

bulletspeed = 20


#Player Movement
def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -280:
        x = -280
    player.setx(x)
def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 280:
        x = 280
    player.setx(x)

#Bullets
bullets = []

def fire_bullet():
    # Creating the player's bullet
    bullet = turtle.Turtle()
    bullet.shape("bullet.gif")
    bullet.penup()
    bullet.speed(0)
    bullet.setposition(player.xcor(), player.ycor())
    bullets.append(bullet)
    # winsound.PlaySound("explosion-e+b.wav", winsound.SND_ASYNC) #sound for windows
    # os.system("aplay Fire.wav&")  # sound for linux
    # playsound('Fire.wav')
    # Start new Threads to play sound
    newThread = playFireSoundThread('Fire.wav')
    newThread.start()

def update_bullet():
    for eachBullet in bullets:
        currentX = eachBullet.xcor()
        currentY = eachBullet.ycor()
        eachBullet.setposition(currentX, currentY + bulletspeed)
        # print("Setting Bullet Pos")

# For collision between enemy and bullet
def isCollision(t1, t2, distThreshold):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < distThreshold:
        return True
    else:
        return False

def update_enemies():
    for enemy in enemies:
        #Update Game Status inside updating enemies, or else bullets will be really slow
        update_bullet()
        check_collisions()
        destroy_bullets()
        # Move the enemy
        global enemyspeed
        global timer
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        # Move the enemy back and down
        if enemy.xcor() > 270:
            # Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction
            enemyspeed *= -1

        if enemy.xcor() < -270:
            # Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction
            enemyspeed *= -1

def check_collisions():
    for enemy in enemies:
        for bullet in bullets:
            if isCollision(bullet, enemy, 25):
                global score
                # winsound.PlaySound("explosion-e+b.wav", winsound.SND_ASYNC) #sound for windows
                # os.system("aplay explosion-e+b.wav&")  # sound for linux
                newThread = playFireSoundThread('exploded.wav')
                newThread.start()

                # Reset the bullet
                bullet.hideturtle()
                bulletstate = "ready"
                bullet.setposition(0, -400)
                # Reset the enemy
                # x = random.randint(-200, 200)
                # y = random.randint(100, 250)
                # enemy.setposition(x, y)
                #Destroy the enemy

                # update the score
                score += 10
                scorestring = "Score: %s" %score
                score_pen.clear()
                score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
                enemy.hideturtle()
                bullet.hideturtle()
                enemies.remove(enemy)
                bullets.remove(bullet)
                if len(enemies) == 0:
                    spawn_enemies()
                break
    # check for a collision between the player and enemy
        if isCollision(player, enemy, 40):
            # winsound.PlaySound("explosion-e+p.wav", winsound.SND_ASYNC) #sound for windows
            os.system("aplay explosion-e+p.wav&")  # sound for linux
            player.hideturtle()
            for e in enemies:
                e.hideturtle()
            # wn.bgpic("end.gif")
            break

def destroy_bullets():
    for bullet in bullets:
        if bullet.ycor() > 270:
            bullet.hideturtle()
            bullets.remove(bullet)

#Binding Event!!! this time in turtle
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")

spawn_enemies()

while True:
    update_enemies()









