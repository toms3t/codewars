class PokerHand(object):

    CARDMAP = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
        '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }

    CARDMAP_REVERSED = {val: key for key, val in CARDMAP.items()}

    def __init__(self, hand):
        self.hand = hand.split()
        self.straight = False
        self.one_pair = False
        self.two_pair = False
        self.two_pair_higher = 0
        self.two_pair_lower = 0
        self.three = False
        self.four = False
        self.result = 0
        self.high_card = None
        self.flush = False
        self.full_house = False
        self.straight_flush = False
        self.royal_flush = False
        self.score = 0
        self.values = []
        self.single_values = []

    def get_card_values(self):
        '''
        This function takes in the hand as a list and parses out the card values, then sorts the values low to high
        :return: Returns the numerical values of the cards in a given hand (Jack = 11, Queen = 12, King = 13, Ace = 14)
        '''

        for card in self.hand:
            if card[0] in PokerHand.CARDMAP:
                self.values.append(PokerHand.CARDMAP[card[0]])
        self.values.sort()
        return self.values

    def identify_hand(self):
        '''
        This function identifies the best hand that the player can make with 5 cards
        :return: Does not return a value, only sets a object attribute to True if a hand (i.e. Two Pair) is identified
        '''

        i = 0
        highest = 0
        high_suit = ''
        self.values = self.get_card_values()
        self.single_values = sorted([x for x in self.values if self.values.count(x) == 1])
        prev = self.values[0]

        # Identifying High Card
        for card in self.hand:
            if PokerHand.CARDMAP[card[0]] > highest:
                highest = PokerHand.CARDMAP[card[0]]
                high_suit = card[-1]
        self.high_card = str(PokerHand.CARDMAP_REVERSED[highest]) + high_suit

        # Identifying a Straight
        self.score = self.values[-1]
        for val in self.values[1:]:
            if prev + 1 == val:
                prev = val
                i += 1
        if prev == self.values[-1] and i == 4:
            self.straight = True
            self.score = self.values[-1]

        # Identifying matched cards (one-pair / two-pair / three-of-a-kind / four-of-a-kind)
        for val in self.values:
            if self.values.count(val) == 2:
                self.one_pair = True
                self.score = val
                # self.score = self.tiebreaker(val)
            elif self.values.count(val) == 3:
                self.three = True
                self.score = val
            elif self.values.count(val) == 4:
                self.four = True
                self.score = val
        if self.values.count(self.values[1]) == 2 and self.values.count(self.values[3]) == 2:
            self.two_pair = True
            self.two_pair_higher = max(self.values[1], self.values[3])
            self.two_pair_lower = min(self.values[1], self.values[3])
            self.score = self.two_pair_higher

        # Identifying a Full House
        if self.values.count(self.values[0]) == 3:
            if self.values.count(self.values[-1]) == 2:
                self.full_house = True
        elif self.values.count(self.values[0]) == 2:
            if self.values.count(self.values[-1]) == 3:
                self.full_house = True

        # Identifying a Flush
        concat = ''.join(self.hand)
        if concat.count('C') == 5:
            self.flush = True
            self.score = self.values[-1]
        elif concat.count('D') == 5:
            self.flush = True
            self.score = self.values[-1]
        elif concat.count('H') == 5:
            self.flush = True
            self.score = self.values[-1]
        elif concat.count('S') == 5:
            self.flush = True
            self.score = self.values[-1]

        # Identifying a Straight Flush or Royal Flush
        if self.straight == True and self.flush == True:
            self.straight_flush = True
            self.score = self.values[-1]
            if sum(self.values) == 60:
                self.royal_flush = True
                self.score = 100

    def get_hand_value(self):
        '''
        This function assigns a value to the best hand identified by "identify hand()".
        :return: Returns the self.result value which is used to rank the value of a hand
        '''
        if self.royal_flush:
            self.result = 10
            return self.result
        if self.straight_flush:
            self.result = 9
            return self.result
        if self.four:
            self.result = 8
            return self.result
        if self.full_house:
            self.result = 7
            return self.result
        if self.flush:
            self.result = 6
            return self.result
        if self.straight:
            self.result = 5
            return self.result
        if self.three:
            self.result = 4
            return self.result
        if self.two_pair:
            self.result = 3
            return self.result
        if self.one_pair:
            self.result = 2
            return self.result
        if self.high_card:
            self.result = 1
            return self.result

    def tiebreaker(self, other_hand):
        '''
        This function determines the winning hand (breaks tie) if both hands are deemed the same (i.e. both one pair).
        :param other_hand: Separate object of type PokerHand class to compare with Self
        :return: String('Win','Loss','Tie') is returned when a tiebreaker is needed (both hands have same result)
        '''
        if self.one_pair:
            kicker = self.find_highest_kicker(other_hand)
            if 'self' in kicker:
                return 'Win'
            elif 'other' in kicker:
                return 'Loss'
            else:
                return 'Tie'
        if self.two_pair:
            if self.two_pair_lower > other_hand.two_pair_lower:
                return 'Win'
            elif self.two_pair_lower < other_hand.two_pair_lower:
                return 'Loss'
            else:
                kicker = self.find_highest_kicker(other_hand)
                if 'self' in kicker:
                    return 'Win'
                elif 'other' in kicker:
                    return 'Loss'
        if self.flush:
            kicker = self.find_highest_kicker(other_hand)
            if 'self' in kicker:
                return 'Win'
            elif 'other' in kicker:
                return 'Loss'
            else:
                return 'Tie'
        if self.score == other_hand.score:
            for val in self.values[::-1]:
                if val != self.score:
                    self.score = val
                    break
            for val in other_hand.values[::-1]:
                if val != other_hand.score:
                    other_hand.score = val
                    break
        if self.high_card:
            kicker = self.find_highest_kicker(other_hand)
            if 'self' in kicker:
                return 'Win'
            elif 'other' in kicker:
                return 'Loss'
            else:
                return 'Tie'
        if self.score > other_hand.score:
            return "Win"
        elif self.score < other_hand.score:
            return "Loss"
        return "Tie"

    def find_highest_kicker(self, other_hand):
        '''
        This function determines the card in the hand that is the highest
        kicker (card that is not part of the winning set of cards).
        :param other_hand: Separate object of type PokerHand class to compare with Self
        :return: Returns "self" or "other_hand" (whichever had highest kicker) and the value of the card
        '''
        for x, y in list(zip(self.single_values, other_hand.single_values))[::-1]:
            if x > y:
                return 'self' + str(x)
            elif x < y:
                return 'other_hand' + str(y)
        return 'Tie'

    def compare_with(self, other_hand):
        '''
        This function compares one hand to another and returns "Win", "Loss", or "Tie" from the perspective of self
        :param other_hand: Separate object of type PokerHand class to compare with Self
        :return: String('Win', 'Loss', 'Tie')
        '''
        self.identify_hand()
        other_hand = PokerHand(other_hand)
        other_hand.identify_hand()
        self.result = self.get_hand_value()
        other_hand.result = other_hand.get_hand_value()
        if self.full_house:
            for val in self.values:
                if self.values.count(val) == 3:
                    self.score = val
            for val in other_hand.values:
                if other_hand.values.count(val) == 3:
                    other_hand.score = val

        if self.result > other_hand.result:
            return "Win"
        if self.result < other_hand.result:
            return 'Loss'

        # Tiebreakers
        if self.result == other_hand.result:
            if self.score > other_hand.score:
                return 'Win'
            elif self.score < other_hand.score:
                return 'Loss'
            else:
                if self.high_card:
                    return self.tiebreaker(other_hand)
                if self.one_pair:
                    return self.tiebreaker(other_hand)
                if self.two_pair:
                    return self.tiebreaker(other_hand)
                if self.flush:
                    return self.tiebreaker(other_hand)

# a = PokerHand('5H 5S 5C AD TS')
# print(a.compare_with('QH QS QH 9D TS'))
