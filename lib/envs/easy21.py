import gym
import numpy as np
from gym import spaces
from gym.utils import seeding


class Easy21Env(gym.Env):
    '''Easy21 game.
    
    Version of the Assignment provided by David Silver's RL Course

    - The game is played with an infinite deck of cards (i.e. cards are sample with replacement)
    - Each draw from the deck results in a value between 1 and 10 (uniforml distributed) with a colour of red (probability 1/3) or black (probability 2/3).
    - There are no aces or picture (face) cards in this game
    - At the start of the game both the player and the dealer draw one *black* card (fully observed)
    - Each turn the player may either *stick* or *hit*
    - If the player *hits* then she draws another card from the deck
    - If the player *sticks* she receives no further cards
    - The values of the player’s cards are added (black cards) or subtracted (red cards)
    - If the player’s sum exceeds 21, or becomes less than 1, then she “goes bust” and loses the game (reward -1)
    - If the player sticks then the dealer starts taking turns. The dealer always sticks on any sum of 17 or greater, and hits otherwise. If the dealer goes bust, then the player wins; otherwise, the outcome – win (reward +1), lose (reward -1), or draw (reward 0) – is the player with the largest sum.
    
    Methods:
        step
        reset
        
    '''
    action_space = spaces.Discrete(2)  # 1: hit, 0: stick
    # action_space = spaces.Discrete(2)
    
    winner_to_reward = {
        'player' :  1,
        'dealer' : -1,
        'none'   :  0,
        ''       :  0
    }
    
    def __init__(self):
        self._seed()
        self.reset()
    
    def reset(self):
        self._player = self._init_card(self.np_random)
        self._dealer = self._init_card(self.np_random)
        self.winner = ''
        self.is_terminate = False
        return self._get_state()
    
    def step(self, action):
        '''Get one time step forward.
        
        Args:
            action
        Returns:
            next state
            reward
            is_terminate
            DEBUG_INFO
        '''
        assert self.action_space.contains(action)
        if action:
            self._hit()
            if self.winner != '':
                self.is_terminate = True
        else:
            self._stick()
            self.is_terminate = True
        return  self._get_state(), self.winner_to_reward[self.winner], self.is_terminate, {}
    
    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
    
    @staticmethod
    def _generate_card(np_random):
        '''generate a card range from 1 to 10 with 2/3 probability 
                    and range from -1 to -10 with 1/3 probability  
        '''
        return np_random.randint(1, 11) * -int(((np_random.randint(0, 3) % 2) - 1. / 2) * 2)
    
    @staticmethod
    def _init_card(np_random):
        '''generate a positive integer between 1 and 10
        
        Return: a list
            list[0]: the first card of player
        '''
        return [np_random.randint(1, 11)]
    
    def _stick(self):
        while sum(self._dealer) < 17 and sum(self._dealer) > 0:
            self._dealer.append(self._generate_card(self.np_random))
        dealer_current_point = sum(self._dealer)
        player_current_point = sum(self._player)
        if dealer_current_point > 21 or dealer_current_point < 1:
            self.winner = 'player'
        elif dealer_current_point < player_current_point:
            self.winner = 'player'
        elif dealer_current_point == player_current_point:
            self.winner = 'none'
        else:
            self.winner = 'dealer'
            
    def _hit(self):
        self._player.append(self._generate_card(self.np_random))
        current_point = sum(self._player)
        if current_point > 21 or current_point < 1:
            self.winner = 'dealer'
            
    def _get_state(self):
        '''
        Return current game state: 
        player's point and dealer's first card 
        '''
        return (sum(self._player), self._dealer[0])




if __name__ == '__main__':
    env = Easy21Env()
    s = env.reset()
    print(s)
    done = False
    while not done:
        s, r, done, _ = env.step(env.action_space.sample())
        print(s, r)