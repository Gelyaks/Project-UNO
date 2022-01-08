import pygame
from random import shuffle, choice


colors = ['yellow', 'red', 'blue', 'green']
num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
fon = pygame.image.load("data/fon.jpg")


class Card(object):
    def __init__(self, suit, rank, in_deck=False, image=None):
        if suit in colors and rank in num:
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


class Deck(object):
    def __init__(self):
        self.cards = []
        for i in range(8):
            c = choice(colors)
            n = choice(num)
            self.cards.append(Card(c, n, in_deck=True))
        self.removed = []

    def __str__(self):
        return str([str(card) for card in self.cards])

    def draw(self, rng=1):
        drawn_cards = self.cards[:rng]
        for card in drawn_cards:
            card.in_deck = False
        del self.cards[:rng]
        self.removed.append(drawn_cards)
        return drawn_cards

    def deck_shuffle(self):
        shuffle(self.cards)


class Player(object):
    def __init__(self, name, hand=None, score=0, turn=False):
        self.name = name
        self.hand = hand
        self.score = score
        self.turn = turn
        self.selected_card = None

    def __str__(self):
        return str(self.name)

    def remove_from_hand(self, card):
        if card and card in self.hand:
            position = self.hand.index(card)
            del self.hand[position]
            return card
        return None


def show_hand(screen, player):
    x, y, space_between_cards = 5, 482, 5
    for card in player.hand:
        card.position_x, card.position_y = x, y
        screen.blit(card.image, (x, y))
        x += card.horizontal_demension + space_between_cards


def select_card(player, mouse_x, mouse_y):
    if mouse_x:
        for card in player.hand:
            lower_x, upper_x = (card.position_x, card.position_x + card.horizontal_demension)
            lower_y, upper_y = (card.position_y, card.position_y + card.vertical_demension)
            if mouse_x > lower_x and mouse_x < upper_x:
                if mouse_y > lower_y and mouse_y < upper_y:
                    player.selected_card = card


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
    y = player.selected_card.position_y
    screen.blit(player.selected_card.image, (x, y))


def update_selected_card_position(player, new_y_position):
    if player.selected_card:
        player.selected_card.position_y = new_y_position


def flip_turns(player1, player2):
    pass


def turn(player, mouse_x, mouse_y, new_y_position):
    select_card(player, mouse_x, mouse_y)
    player.remove_from_hand(player.selected_card)
    update_selected_card_position(player, new_y_position)


def main():
    sc_width, sc_height = 800, 650
    selected_card_y_pos_player_1 = 170
    selected_card_y_pos_player_2 = 170
    delay_time_ms = 1000
    number_of_cards = 8
    turn_count = 1
    deck = Deck()
    deck.deck_shuffle()
    player1 = Player('Ivan', hand=deck.draw(number_of_cards), turn=True)
    player2 = Player('Serg', hand=deck.draw(number_of_cards))
    pygame.init()
    screen = pygame.display.set_mode((sc_width, sc_height))
    load_card_images(player1)
    load_card_images(player2)
    game = True
    while game:
        screen.fill('white')
        screen.blit(fon, (0, 0))
        mouse_x, mouse_y = None, None
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game = False
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()

        if player1.turn:
            show_hand(screen, player1)
            turn(player1, mouse_x, mouse_y, selected_card_y_pos_player_1)
            if player1.selected_card:
                flip_turns(player1, player2)
        else:
            # Здесь будет ИИ
            pass

        if player1.selected_card:
            play_selected_card(screen, player1)
        pygame.display.update()

        if not player1.hand and not player2.hand:
            pygame.display.update()
            pygame.time.delay(delay_time_ms)
            game = False


if __name__ == '__main__':
    main()