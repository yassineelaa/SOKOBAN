#!/usr/bin/env python3
import pygame
import sys
import yaml
from pygame.locals import *
from main import Sokoban  # On garde l'import de la classe Sokoban depuis main.py

# Charger la configuration depuis le fichier config.yaml
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Initialisation de Pygame et définition de la fenêtre du menu
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sokoban - Menu Principal")

# Couleurs et polices
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
TITLE_FONT = pygame.font.SysFont("Comic Sans MS", 64)
MENU_FONT = pygame.font.SysFont("Comic Sans MS", 40)

# Définition des options du menu
menu_items = ["Nouvelle Partie", "Options", "Crédits", "Quitter"]
selected_item = 0

def draw_menu(selected):
    """Affiche l'écran du menu avec l'élément sélectionné."""
    screen.fill(BLACK)
    # Affichage du titre
    title_text = TITLE_FONT.render("Sokoban", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_text, title_rect)
    # Affichage des options du menu
    for index, item in enumerate(menu_items):
        color = WHITE if index == selected else GRAY
        menu_text = MENU_FONT.render(item, True, color)
        text_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, 250 + index * 60))
        screen.blit(menu_text, text_rect)
    pygame.display.flip()

def options_menu():
    """Affiche un exemple simple de menu Options."""
    running = True
    while running:
        screen.fill(BLACK)
        options_text = MENU_FONT.render("Menu Options (ECHAP pour revenir)", True, WHITE)
        text_rect = options_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(options_text, text_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

def credits_screen():
    """Affiche l'écran des crédits."""
    running = True
    while running:
        screen.fill(BLACK)
        credits_lines = [
            "Crédits",
            "Développé par : EL-AASMI Yassine",
            "Inspiré par des tutoriels Sokoban",
            "Appuyez sur une touche pour revenir..."
        ]
        for i, line in enumerate(credits_lines):
            credit_text = MENU_FONT.render(line, True, WHITE)
            text_rect = credit_text.get_rect(center=(SCREEN_WIDTH // 2, 150 + i * 50))
            screen.blit(credit_text, text_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.QUIT):
                running = False

def main_menu():
    """Boucle principale du menu."""
    global selected_item
    clock = pygame.time.Clock()
    menu_active = True
    while menu_active:
        draw_menu(selected_item)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Navigation dans le menu (adapté pour QWERTY et AZERTY)
                if event.key in (pygame.K_UP, pygame.K_z):
                    selected_item = (selected_item - 1) % len(menu_items)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected_item = (selected_item + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    # Exécuter l'action associée à l'option sélectionnée
                    if menu_items[selected_item] == "Nouvelle Partie":
                        Sokoban(config).play()
                    elif menu_items[selected_item] == "Options":
                        options_menu()
                    elif menu_items[selected_item] == "Crédits":
                        credits_screen()
                    elif menu_items[selected_item] == "Quitter":
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()
