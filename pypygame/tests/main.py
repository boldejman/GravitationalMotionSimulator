import pygame as pg
import math


def blitRotate(surf, image, pos, originPos, angle, zoom):
    # calculate the axis aligned bounding box of the rotated image
    w, h = image.get_size()
    box = [pg.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot
    pivot = pg.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    move = (-originPos[0] + min_box[0] - pivot_move[0], -originPos[1] - max_box[1] + pivot_move[1])
    origin = (pos[0] + zoom * move[0], pos[1] + zoom * move[1])

    # get a rotated image
    rotozoom_image = pg.transform.rotozoom(image, angle, zoom)

    # rotate and blit the image
    surf.blit(rotozoom_image, origin)

    # draw rectangle around the image


def rightSide(x, y, v, u, m=1, k=1):
    F1 = [-k*x/(x**2+y**2)**1.5, -k*y/(x**2+y**2)**1.5]
    F2 = [-k*(x-1)/((x-1)**2+y**2)**1.5, -k*y/((x-1)**2+y**2)**1.5]
    derv = (F1[0]+F2[0])/m
    deru = (F1[1]+F2[1])/m
    derx = v
    dery = u
    return [derx, dery, derv, deru]


def RungeKutta(x0, y0, v0, u0, t0, t, h=0.00001):
    # number of iterating process
    n = int((t-t0)/h)

    # define y_k as y(x_k), where y(x) is function that we are looking for
    x_k = x0
    y_k = y0
    v_k = v0
    u_k = u0
    x_values = [x0*100]
    y_values = [y0*100]
    v_values = [v0*100]
    u_values = [u0*100]

    for i in range(1, n+1):
        k1 = [h * elem for elem in rightSide(x_k, y_k, v_k, u_k)]
        k2 = [h * elem for elem in rightSide(x_k + h*k1[0]/2, y_k + h*k1[1]/2, v_k + h*k1[2]/2, u_k + h*k1[3]/2)]
        k3 = [h * elem for elem in rightSide(x_k + h*k2[0]/2, y_k + h*k2[1]/2, v_k + h*k2[2]/2, u_k + h*k2[3]/2)]
        k4 = [h * elem for elem in rightSide(x_k + h*k3[0], y_k + h*k3[1], v_k + h*k3[2], u_k + h*k3[3])]

        x_k += (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6
        y_k += (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6
        v_k += (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]) / 6
        u_k += (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3]) / 6
        x_values.append(x_k*100)
        y_values.append(y_k*100)
        v_values.append(v_k*100)
        u_values.append(u_k*100)

    return x_values, y_values, v_values, u_values


x0 = 1
y0 = 0.4
v0 = 1
u0 = -0.5

x, y, v, u = RungeKutta(x0, y0, v0, u0, 0, 20)
print(v[1],u[1])
print(math.atan(u[1000]/v[1000])*180/math.pi)

def main():

    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((1080, 720))
    pg.display.set_caption("some program")
    image = pg.image.load("../../figures/rocket3.png")
    image = pg.transform.rotate(image, -45)
    w, h = image.get_size()
    i = 0
    angle, zoom = 10, 1
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        pg.draw.rect(screen, (210, 210, 210), (0, 0, 840, 720))
        pg.draw.rect(screen, (210, 190, 190), (840, 0, 1080, 720))
        pg.draw.circle(screen, (255, 255, 255), (960, 600), 120)

        pos = (x[i*1000]+500, y[i*1000]+500)
        angle = math.atan(u[i*1000]/v[i*1000])*180/math.pi
        i += 1
        blitRotate(screen, image, pos, (w / 2, h / 2), angle, zoom)
        pg.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    main()
