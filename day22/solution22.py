from aoclib import read_input


class Game:
    def __init__(self, lines):
        self.players = []
        current_player = None
        self.hands = []
        self.winner = None
        for line in lines:
            if ':' in line:
                current_player = Player(line[:-1])
                self.players.append(current_player)
            else:
                current_player.deck.append(int(line))

    def play(self):
        r = 0
        while not self.game_over():
            hand = Hand(self)
            r = hand.ix
            print(hand)
        else:
            self.winner = self.get_not_empty_players().pop()
            print('GAME OVER!')
        return self

    def game_over(self):
        return len(self.get_not_empty_players()) == 1

    def get_not_empty_players(self):
        return [p for p in self.players if len(p.deck)]


class Hand:
    ix = 0

    def __init__(self, game: Game):
        Hand.ix += 1
        self.ix = Hand.ix
        self.players = [PlayerInHand(p, self) for p in game.players]

        cards = [p.card for p in self.players]
        winning_card = max(cards)
        winning_card_ix = cards.index(winning_card)
        self.winner = self.players[winning_card_ix].get_prize(sorted(cards)[::-1])

    def __str__(self):
        decks = []
        cards = []
        for p in self.players:
            deck = ', '.join([str(x) for x in p.deck_start])
            name = p.player.name
            decks.append("{name}'s deck: {deck}".format(name=name, deck=deck))
            cards.append("{name}'s card: {card}".format(name=name, card=p.card))
        dd = '\n'.join(decks)
        cc = '\n'.join(cards)
        w = '{name} wins the round!'.format(name=self.winner.player.name)
        return '-- Round -- {ix}\n{dd}\n{cc}\n{w}\n'.format(ix=self.ix, dd=dd, cc=cc, w=w)


class Player:
    def __init__(self, name):
        self.name = name
        self.deck = []

    def get_score(self):
        deck = [0] + self.deck[::-1]
        return sum([ix * deck[ix] for ix in range(len(deck))])

    def __str__(self):
        return "{name}'s deck: {deck}".format(name=self.name, deck=', '.join([str(x) for x in self.deck]))


class PlayerInHand:
    def __init__(self, player: Player, hand: Hand):
        self.player = player
        self.hand = hand
        self.deck_start = player.deck[:]
        self.card = player.deck.pop(0)
        self.win = []

    def get_prize(self, cards):
        self.win = cards
        self.player.deck += cards
        return self


def part_1(data):
    game = Game(data).play()
    score = game.winner.get_score()
    print('SCORE = ', score)
    return score


def part_2(data):
    return 0


def solve():
    return (
        part_1(read_input(True)) == 306 and part_1(read_input()),
        part_2(read_input(True)) == 0 and part_2(read_input()),
    )


if __name__ == '__main__':
    print(solve())
