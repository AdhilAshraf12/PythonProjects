import pygame
import sys
import math
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os


screen = pygame.display.set_mode((800,800))

class spot:
    def __init__(self,x,y):
        self.i = x
        self.j = y