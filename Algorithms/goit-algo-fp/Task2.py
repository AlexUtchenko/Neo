import turtle


def draw_pythagoras_tree(t, order, size, angle):
    if order == 0:
        return
    t.forward(size)
    t.left(angle)
    draw_pythagoras_tree(t, order-1, size * 0.7, angle) # рекурсія по гілці 1
    t.right(2 * angle)
    draw_pythagoras_tree(t, order-1, size * 0.7, angle) # рекурсія по гілці 2
    t.left(angle)
    t.backward(size)

def main():

    order = int(input("Введіть рівень рекурсії (int): ")) # запит глибини рекурсії
    size = 100
    angle = 45

    window = turtle.Screen()
    window.bgcolor("white")
    window.title("Дерево Піфагора")

    t = turtle.Turtle()
    t.color("green")
    t.speed(0)
    t.left(90) 

    draw_pythagoras_tree(t, order, size, angle)

    window.mainloop()


if __name__ == "__main__":
    main()
