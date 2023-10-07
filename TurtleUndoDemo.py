# import package
import turtle

# set speed
turtle.speed(1)


# motion
turtle.forward(100)
turtle.pendown()
turtle.forward(100)
radius = 5
a = turtle.undobufferentries()
turtle.forward(100)
turtle.pendown()
turtle.forward(100)
# undo previous motion

for i in range(2):
    turtle.undo()

print(turtle.undobufferentries())


