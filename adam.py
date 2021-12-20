from ahk import AHK
from time import time, sleep
import numpy as np
import random 

comments = ['Love the colour 0.0!',
        'Amazing work haha!',
        'Amazing work!',
        'Amazing work!',
        'Awesome post :))',
        'Awesome post!',
        'Awesome post!',
        'Looks awesome!',
        'LOL This is inspiring!',
        'Honestly this is amazing',
        'please keep it up!',
        'Omgg so gorgeous!!',
        'THIS\'S SO AMAZING LOVE IT!',
        'absolutely stunning',
        'Nice one!',
        'Love that lighting so much.',
        'Amazing work!',
        'ON FIRE! 100/100!',
        'Lovely!',
        'great content!',
        'great content!',
        'Great content!!',
        u'awesome content!!! :thumbsup:',
        u'Awesome content!! :thumbsup:',
        u'100/100 love it :thumbsup:!',
        u'This is just incredible :heart_eyes',
        u'amazing shot! :heart_eyes:']

# OOP Review:
# class is a blueprint and an instance is an ovject that is built from a class and contains real data
class Adam():
    # note: every function inside a class is called a "instance method"
    def __init__(self, likes:int = 20, interact:bool = False, random_offset:bool = True):
        """
        Instance Attributes:
            likes: total likes you want to engage including profile interaction if it's set to True
            interact: set to False by default. Will randomly interact with user profile if it's set to True
            random_offset: randomly deflate likes within its 70% - 100%
        """
        self.ahk = AHK()
        if random_offset:
            self.likes = int(likes * np.random.uniform(low=0.7, high=1.0))
        else:
            self.likes = likes
        self.interact = interact
        self.random_offset = random_offset

        # internal trackers
        self.liked = 0
        self.skipped = 0
        self.start_time = time()
        self.interacting = False
        self.terminate = False

    
    # Pythonic way to define print(Object)
    def __str__(self):
        # define engagement rate (handle zero division)
        try:
            engagement = round(self.liked / (self.liked + self.skipped), 3)
        except ZeroDivisionError:
            engagement = -1

        e_time = round(time() - self.start_time, 2)

        # print out a summary of the current running state in console
        summary = f"""
        elapsed time: {e_time}s | total likes: {self.likes}
        current likes: {self.liked} | current skipped: {self.skipped} | engagement rate: {engagement}"""

        return summary
    
    def like(self, prob: float):
        """
        like a photo and go to the next one with prob% chance
        """
        if random.randrange(0, 100) <= prob:
            # double click to like
            self.ahk.mouse_move(2000, 1000, speed=10, blocking=True)
            self.ahk.double_click()
            self.rsleep(4)

            # certain chance to interact with user profile

            # certain chance to comment

            # update the tracker
            self.liked +=1
        else:
            self.skipped +=1

        if self.liked >= self.likes:
            self.terminate = True
            return

        # click next arrow icon
        self.ahk.mouse_move(2675, 943, speed=10, blocking=True)
        self.ahk.click()
        self.rsleep(4)


    def interact(self, prob: float):
        pass

    def comment(self, prob: float):
        pass

    def rsleep(self, sec:int):
        """randomly sleep b/w 70% - 100% seconds"""
        sleep(sec * np.random.uniform(low=0.5, high=1.5))


if __name__ == '__main__':
    adam = Adam(likes=5, interact=False, random_offset=True)

    # main code run()
    while not adam.terminate:
        print(adam) # log progress
        adam.like(random.randrange(40, 80)) # randomly generate probability from 50% to 100%
        
    
    