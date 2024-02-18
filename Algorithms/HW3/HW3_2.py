import turtle

def koch_snowflake(turtle, length, depth):
  """
  Функція для малювання сніжинки Коха рекурсивно
    length: Довжина сторони трикутника
    depth: Глибина рекурсії
  """

  if depth == 0:
    turtle.forward(length)
  else:
    koch_snowflake(turtle, length / 3, depth - 1)
    turtle.left(60)
    koch_snowflake(turtle, length / 3, depth - 1)
    turtle.right(120)
    koch_snowflake(turtle, length / 3, depth - 1)
    turtle.left(60)
    koch_snowflake(turtle, length / 3, depth - 1)


depth = int(input('Введіть глибину рекурсії (int): '))

# Створення нового об'єкта turtle
t = turtle.Turtle()

# Встановлення параметрів
t.speed(0)
t.pencolor("black")
t.fillcolor("lightblue")

# Малювання сніжинки Коха на 3 сторонах рівностороннього трикутника з кутом повороту 180-60=120 градусів
for i in range(3): # кількість сторін (3)
  koch_snowflake(t, 300, depth)
  t.right(120) # кут повороту (120)

# Завершення роботи turtle
turtle.done()
