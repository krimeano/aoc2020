from aoclib import read_input


class Counter:
    def __init__(self):
        self.val = 0

    def __int__(self):
        self.val += 1
        return self.val


class Game:
    def __init__(self):
        self.players = []
        self.hands = []
        self.winner = None
        self.handCounter = Counter()

    def init_players(self, lines):
        """
        :param list[str] lines:
        :return:
        """
        self.players = []
        current_player = None
        for line in lines:
            if ':' in line:
                current_player = Player(line[:-1])
                self.players.append(current_player)
            else:
                current_player.deck.append(int(line))
        return self

    def set_players(self, players):
        """
        :param list[Player] players:
        :return:
        """
        self.players = players
        return self

    def play(self):
        while self.is_finite() and not self.game_over():
            hand = self.get_hand()
            # print(hand)
        else:
            self.winner = self.get_not_empty_players().pop(0)
            print('GAME OVER!')
        return self

    def get_hand(self):
        return Hand(self)

    def game_over(self):
        return len(self.get_not_empty_players()) == 1

    def get_not_empty_players(self):
        return [p for p in self.players if len(p.deck)]

    def is_finite(self):
        return True


class Hand:
    def __init__(self, game: Game):
        self.ix = int(game.handCounter)
        self.players = [PlayerInHand(p, self) for p in game.players]
        self.winner = None
        self.define_winner()

    def define_winner(self):
        cards = [p.card for p in self.players]
        winning_card = max(cards)
        winning_ix = cards.index(winning_card)
        self.winner = self.players[winning_ix].get_prize(sorted(cards)[::-1])

    def __str__(self):
        decks = []
        cards = []
        for p in self.players:
            deck = ', '.join([str(p.card)] + [str(x) for x in p.deck])
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
        self.card = player.deck.pop(0)
        self.deck = player.deck[:]
        self.win = []

    def get_prize(self, cards):
        self.win = cards
        self.player.deck += cards
        return self


def part_1(data):
    game = Game().init_players(data).play()
    score = game.winner.get_score()
    return score


class GameRecursive(Game):
    games_counter = Counter()

    def __init__(self):
        super().__init__()
        self.ix = int(GameRecursive.games_counter)
        self.decks_states = set()
        print('\n=== Game {ix} ==='.format(ix=self.ix))

    def get_hand(self):
        return HandRecursive(self)

    def is_finite(self):
        state = tuple(tuple(x.deck) for x in self.players)
        if state in self.decks_states:
            print('GAME IS INFINITE!')
            return False
        self.decks_states.add(state)
        return True


class HandRecursive(Hand):
    def __init__(self, game: GameRecursive):
        super().__init__(game)

    def define_winner(self):
        is_recursive = not sum([p.card > len(p.deck) for p in self.players])

        if not is_recursive:
            return super().define_winner()

        mem_decks = [x.player.deck[:] for x in self.players]
        mem_cards = [p.card for p in self.players]
        print('RECURSIVE!', mem_cards, mem_decks)
        for ix in range(len(self.players)):
            p = self.players[ix]
            p.player.deck = p.player.deck[:p.card]

        sub_game = GameRecursive().set_players([x.player for x in self.players]).play()
        self.winner = self.players[[x.player for x in self.players].index(sub_game.winner)]
        print('The winner of game {ix} is {player}'.format(ix=sub_game.ix, player=sub_game.winner.name))
        for ix in range(len(self.players)):
            self.players[ix].player.deck = mem_decks[ix][:]
        players = sorted(self.players, key=lambda p: p.player.name != sub_game.winner.name)

        self.winner.get_prize([p.card for p in players])


def part_2(data):
    GameRecursive.games_counter = Counter()
    game = GameRecursive().init_players(data).play()
    score = game.winner.get_score()
    print('GAME SCORE', score)
    return score


def solve():
    return (
        part_1(read_input(True)) == 306 and part_1(read_input()),
        part_2(read_input(True, '2')) == 105 and part_2(read_input(True)) == 291 and part_2(read_input()),
    )


if __name__ == '__main__':
    print(solve())
