import pygame
import sqlite3
from random import choice
from win import win
from lost import lost

numbers = []
colors = []
conn = sqlite3.connect('cards.db')
cur = conn.cursor()
res = cur.execute("""SELECT color FROM cards""").fetchall()
res1 = cur.execute("""SELECT num FROM cards""").fetchall()
for i in res:
    if i[0] not in colors:
        colors.append(i[0])

for i in res1:
    if i[0] not in numbers:
        numbers.append(i[0])


class Card(object):
    def __init__(self, suit, rank, in_deck=False, image=None):
        if suit in colors and rank in numbers:
            self.rank = rank
            self.suit = suit
        else:
            self.rank = None
            self.suit = None

        self.in_deck = in_deck
        self.image = image
        self.position_x, self.position_y = 0, 0
        self.horizontal_demension = None
        self.vertical_demension = None

    def __str__(self):
        return str(self.rank) + " " + str(self.suit)


class Button():
    def __init__(self, text, x=0, y=0, width=30, height=30):

        self.text = text

        self.image_normal = pygame.Surface((width, height))
        self.image_normal.fill('white')

        self.image_hovered = pygame.Surface((width, height))
        self.image_hovered.fill('grey')

        self.image = self.image_normal
        self.rect = self.image.get_rect()

        font = pygame.font.SysFont('Arial', 45)

        text_image = font.render(text, True, 'black')
        text_rect = text_image.get_rect(center=self.rect.center)

        self.image_normal.blit(text_image, text_rect)
        self.image_hovered.blit(text_image, text_rect)
        self.rect.topleft = (x, y)

        self.hovered = False

    def update(self):
        if self.hovered:
            self.image = self.image_hovered
        else:
            self.image = self.image_normal

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Deck(object):
    def __init__(self):
        self.cards = []

        for i in range(8):
            c = choice(colors)
            n = choice(numbers)
            self.cards.append(Card(c, n, in_deck=True))
        self.removed = []

    def __str__(self):
        return str([str(card) for card in self.cards])

    def draw(self, range=1):
        """Draw card(s) by removing them from deck"""
        drawn_cards = self.cards[:range]
        for card in drawn_cards:
            card.in_deck = False
        del self.cards[:range]
        self.removed.append(drawn_cards)
        return drawn_cards


class Player(object):
    def __init__(self, hand=None, turn=False):
        self.hand = hand
        self.turn = turn
        self.selected_card = None
        self.last_card = None
        self.count = None

    def remove_from_hand(self, card):
        if card and card in self.hand:
            position = self.hand.index(card)
            del self.hand[position]
            return card
        return None


def show_hand(screen, player):
    x, y, space_between_cards = 5, 482, 5
    a = 0
    for card in player.hand:
        card.position_x, card.position_y = x, y
        screen.blit(card.image, (x, y))
        a += 1
        x += card.horizontal_demension + space_between_cards


def check_loose(player1, player2):
    f3 = False
    for i in player1.hand:
        if i.suit == player2.last_card.suit or i.rank == player2.last_card.rank:
            f3 = True
    if not f3 and len(player1.hand) >= 8:
        you_loose()


def you_loose():
    lost()


def select_card(player, mouse_x, mouse_y):
    if mouse_x:
        for card in player.hand:
            lower_x, upper_x = (card.position_x, card.position_x + card.horizontal_demension)
            lower_y, upper_y = (card.position_y, card.position_y + card.vertical_demension)
            if mouse_x > lower_x and mouse_x < upper_x:
                if mouse_y > lower_y and mouse_y < upper_y:
                    player.selected_card = card


def ui_deck(player2):
    player2.deck = []
    for i in range(8):
        c = choice(colors)
        n = choice(numbers)
        player2.deck.append(Card(c, n))


def load_card_images(player):
    for card in player.hand:
        col = str(card).split()[1]
        num = str(card).split()[0]
        card.image = pygame.image.load(f"Cards/{col}/{num}.png")
        width, height = card.image.get_size()
        card.horizontal_demension = width
        card.vertical_demension = height


def play_selected_card(screen, player):
    x = player.selected_card.position_x = 220
    y = player.selected_card.position_y = 170
    screen.blit(player.selected_card.image, (x, y))
    player.last_card = player.selected_card
    player.selected_card = None


def plus(hand):
    c = choice(colors)
    n = choice(numbers)
    card = Card(c, n, in_deck=True)
    card.image = pygame.image.load(f"Cards/{c}/{n}.png")
    card.horizontal_demension, card.vertical_demension = card.image.get_size()
    hand.append(card)


def check_card(player1, player2):
    if not player2.last_card:
        return True
    elif player1.selected_card.suit != player2.last_card.suit and player1.selected_card.rank != player2.last_card.rank:
        return False
    return True


def white(hand, screen):
    x = len(hand) * 100
    pygame.draw.rect(screen, 'white', (x, 482, 800 - x, 168))


def generate_card(player2, player1):
    color = player1.last_card.suit
    n = player1.last_card.rank
    f1 = False
    c = 0
    while not f1 and c < len(player2.deck):
        if player2.deck[c].suit == c or player2.deck[c].rank == n:
            f1 = True
            card = player2.deck[c]
            del player2.deck[c]
        c += 1
    if not f1:
        card = Card(choice(colors), choice(numbers), in_deck=False)
        while card.suit != color and card.rank != n:
            col = choice(colors)
            if len(col) > 3:
                card = Card(col, choice(numbers), in_deck=False)
                player2.deck.append(card)
    return card


def you_win():
    win()


def main(level):
    deck = Deck()
    pygame.display.set_caption('UNO')
    sc_width, sc_height = 800, 650
    screen = pygame.display.set_mode((sc_width, sc_height))
    fon = pygame.image.load("data/fon.jpg")
    player1 = Player(hand=deck.draw(8), turn=True)
    player2 = Player()
    pygame.init()
    btn1 = Button('+', 750, 430, 40, 40)
    load_card_images(player1)
    game = True
    screen.fill('white')
    screen.blit(fon, (0, 0))
    clock = pygame.time.Clock()
    ui_deck(player2)
    while game:
        mouse_x, mouse_y = None, None
        events = pygame.event.get()
        rules = pygame.image.load('data/fon2.png')
        screen.blit(rules, (550, 50))
        if player2.last_card:
            check_loose(player1, player2)
        for event in events:
            if event.type == pygame.QUIT:
                game = False
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEMOTION:
                btn1.hovered = btn1.rect.collidepoint(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn1.hovered:
                    plus(player1.hand)
        btn1.update()
        btn1.draw(screen)
        if len(player1.hand) == 0:
            you_win()
        pygame.display.update()
        if player1.turn:
            show_hand(screen, player1)
            white(player1.hand, screen)
            f = False
            select_card(player1, mouse_x, mouse_y)
            if player1.selected_card:
                res = check_card(player1, player2)
                if res:
                    player1.remove_from_hand(player1.selected_card)
                    play_selected_card(screen, player1)
                    pygame.display.update()
                    f = True
                    pygame.time.delay(2000)

        if f:
            if len(player2.deck) > 8 and level == 'easy':
                you_win()
            if len(player2.deck) > 23 and level == 'hard':
                you_win()
            if len(player2.deck) == 0:
                you_loose()
            card = generate_card(player2, player1)
            col = card.suit
            num = str(card).split()[0]
            card.image = pygame.image.load(f"Cards/{col}/{num}.png")
            player2.last_card = Card(col, int(num))
            screen.blit(card.image, (220, 170))
            pygame.display.update()
            pygame.time.delay(1200)
        clock.tick(30)
        pygame.display.update()

        if not player1.hand and not player2.hand:
            pygame.display.update()
            pygame.time.delay(1000)
            game = False


if __name__ == '__main__':
    main('easy')
