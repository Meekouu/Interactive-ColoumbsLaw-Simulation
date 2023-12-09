import math
import random
import sys

import pygame
import tkinter as tk
from tkinter import messagebox

from PyPhysics import *


def projectile_motion_window(initial_velocity=50):
    global win, projectile_group, u

    info = pygame.display.Info()

    win = pygame.display.set_mode(SCREEN)
    pygame.display.set_caption('Projectile Motion Simulation')

    clock = pygame.time.Clock()
    FPS = 60

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 87, 34)
    GREEN = (76, 175, 80)
    BLUE = (33, 150, 243)
    ORANGE = (255, 152, 0)
    YELLOW = (255, 235, 59)
    PURPLE = (156, 39, 176)
    AQUA = (0, 188, 212)

    COLORS = [RED, GREEN, BLUE, ORANGE, YELLOW, PURPLE]

    font = pygame.font.SysFont('verdana', 12)

    origin = (20, 400)

    u = initial_velocity
    g = 9.8
    class Projectile(pygame.sprite.Sprite):
        def __init__(self, u, theta):
            super(Projectile, self).__init__()

            self.u = u
            self.theta = toRadian(abs(theta))
            self.x, self.y = origin
            self.color = random.choice(COLORS)

            self.ch = 0
            self.dx = 2

            self.f = self.getTrajectory()
            self.range = self.x + abs(self.getRange())

            self.path = []

        def timeOfFlight(self):
            return round((2 * self.u * math.sin(self.theta)) / g, 2)

        def getRange(self):
            range_ = ((self.u ** 2) * 2 * math.sin(self.theta) * math.cos(self.theta)) / g
            return round(range_, 2)

        def getMaxHeight(self):
            h = ((self.u ** 2) * (math.sin(self.theta)) ** 2) / (2 * g)
            return round(h, 2)

        def getTrajectory(self):
            return round(g / (2 * (self.u ** 2) * (math.cos(self.theta) ** 2)), 4)

        def getProjectilePos(self, x):
            return x * math.tan(self.theta) - self.f * x ** 2

        def update(self):
            if self.x >= self.range:
                self.dx = 0
            self.x += self.dx
            self.ch = self.getProjectilePos(self.x - origin[0])

            self.path.append((self.x, self.y - abs(self.ch)))
            self.path = self.path[-50:]

            pygame.draw.circle(win, self.color, self.path[-1], 5)
            pygame.draw.circle(win, WHITE, self.path[-1], 5, 1)
            for pos in self.path[:-1:5]:
                pygame.draw.circle(win, WHITE, pos, 1)

    projectile_group = pygame.sprite.Group()

    clicked = False
    currentp = None

    theta = -30
    end = getPosOnCircumeference(theta, origin)
    arct = toRadian(theta)
    arcrect = pygame.Rect(origin[0] - 30, origin[1] - 30, 60, 60)



    running = True
    while running:
        win.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False

                if event.key == pygame.K_r:
                    projectile_group.empty()
                    currentp = None

                if event.key == pygame.K_BACKSPACE:
                    running = False
                    pygame.quit()
                    return

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False

                pos = event.pos
                theta = getAngle(pos, origin)
                if -90 < theta <= 0:
                    projectile = Projectile(u, theta)
                    projectile_group.add(projectile)
                    currentp = projectile

            if event.type == pygame.MOUSEMOTION:
                if clicked:
                    pos = event.pos
                    theta = getAngle(pos, origin)
                    if -90 < theta <= 0:
                        end = getPosOnCircumeference(theta, origin)
                        arct = toRadian(theta)

        projectile_group.update()

        pygame.draw.line(win, WHITE, origin, (origin[0] + 250, origin[1]), 2)
        pygame.draw.line(win, WHITE, origin, (origin[0], origin[1] - 250), 2)
        pygame.draw.line(win, AQUA, origin, end, 2)
        pygame.draw.circle(win, WHITE, origin, 3)
        pygame.draw.arc(win, AQUA, arcrect, 0, -arct, 2)

        title = font.render("PyProjectile-Motion-Simulation", True, WHITE)
        fpstext = font.render(f"FPS : {int(clock.get_fps())}", True, WHITE)
        thetatext = font.render(f"Angle : {int(abs(theta))}", True, WHITE)
        degreetext = font.render(f"{int(abs(theta))}°", True, YELLOW)
        win.blit(title, (160, 30))
        win.blit(fpstext, (20, 400))
        win.blit(thetatext, (20, 420))
        win.blit(degreetext, (origin[0] + 38, origin[1] - 20))

        if currentp:
            veltext = font.render(f"Velocity : {currentp.u}m/s", True, WHITE)
            timetext = font.render(f"Time : {currentp.timeOfFlight()}s", True, WHITE)
            rangetext = font.render(f"Range : {currentp.getRange()}m", True, WHITE)
            heighttext = font.render(f"Max Height : {currentp.getMaxHeight()}m", True, WHITE)
            gravitytext = font.render(f"Gravity : -9.8 m/s^2", True, WHITE)


            win.blit(veltext, (WIDTH - 150, 380))
            win.blit(timetext, (WIDTH - 150, 400))
            win.blit(rangetext, (WIDTH - 150, 420))
            win.blit(heighttext, (WIDTH - 150, 440))
            win.blit(gravitytext, (WIDTH - 150, 460))


        pygame.draw.rect(win, (0, 0, 0), (0, 0, WIDTH, HEIGHT), 5)
        clock.tick(FPS)
        pygame.display.update()

    pygame.quit()


def start_simulation():
    pygame.init()
    initial_velocity = float(velocity_entry.get())
    projectile_motion_window(initial_velocity)
    pygame.quit()


pygame.init()
SCREEN = WIDTH, HEIGHT = 500, 512


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() - width) // 2
    y = (window.winfo_screenheight() - height) // 2
    window.geometry(f"400x200+{x}+{y}")


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() - width) // 2
    y = (window.winfo_screenheight() - height) // 2
    window.geometry(f"400x200+{x}+{y}")


root = tk.Tk()
root.title("PyProjectile-Motion-Simulation")

title_label = tk.Label(root, text="PyProjectile-Motion-Simulation", font=("Helvetica", 16))
title_label.pack(pady=20)

velocity_label = tk.Label(root, text="Initial Velocity:")
velocity_label.pack()
velocity_entry = tk.Entry(root)
velocity_entry.insert(0, "50")
velocity_entry.pack()

start_button = tk.Button(root, text="Start Simulation", command=start_simulation)
start_button.pack(pady=30)

center_window(root)
root.mainloop()
