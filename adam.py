"""
How to use:
1) position the window on the RHS of the screen and align with the RIGHT edge of chrome icon in the task bar
2) position VS Code on the LHS of the screen
"""
from ahk import AHK
from time import time, sleep
import numpy as np
import random 

## global variables
comments = [u'Love the colour 0.0!',
        u'Amazing work haha!',
        u'Amazing work!',
        u'Amazing work!',
        u'Awesome post :))',
        u'Awesome post!',
        u'Awesome post!',
        u'Looks awesome!',
        u'LOL This is inspiring!',
        u'Honestly this is amazing',
        u'please keep it up!',
        u'Omgg so gorgeous!!',
        u'THIS\'S SO AMAZING LOVE IT!',
        u'absolutely stunning',
        u'Nice one!',
        u'Love that lighting so much.',
        u'Amazing work!',
        u'ON FIRE! 100/100!',
        u'Lovely!',
        u'great content!',
        u'great content!',
        u'Great content!!',
        u'awesome content!!! :thumbsup:',
        u'Awesome content!! :thumbsup:',
        u'100/100 love it :thumbsup:!',
        u'This is just incredible :heart_eyes:',
        u'amazing shot! :heart_eyes:']

# the screen coordinates after
user_profile_coords=[
    (1400, 400),
    (1400, 800),
    (1400, 1300),
    (1400, 1700),
    (1900, 400),
    (1900, 800),
    (1900, 1300),
    (1900, 1700),
    (2400, 400),
    (2400, 800),
    (2400, 1300),
    (2400, 1700),
]

ahk = AHK()

# OOP Review:
# class is a blueprint and an instance is an ovject that is built from a class and contains real data
class Adam():
    # note: every function inside a class is called a "instance method"
    def __init__(self, likes:int = 20, random_offset:bool = True):
        """
        Instance Attributes:
            likes: total likes you want to engage including profile interaction if it's set to True
            interact: set to False by default. Will randomly interact with user profile if it's set to True
            comment: set to False by default. Will randomly comment liked posts if it's set to True
            random_offset: randomly deflate likes within its 70% - 100%
        """
        if random_offset:
            self.likes = int(likes * np.random.uniform(low=0.7, high=1.0))
        else:
            self.likes = likes
        self.interact = False
        self.comment = False
        self.random_offset = random_offset

        # internal trackers
        self.liked = 0
        self.skipped = 0
        self.interacted = 0
        self.commented = 0
        self.start_time = time()
        self.interacting = False
        self.terminate = False

        # randomization (default interval that reset everytime the function is called)
        self.like_prob = (10, 80)
        self.interact_prob = (10, 20)
        self.comment_prob = (5, 10)

    
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
        elapsed time: {e_time}s | total likes: {self.likes} | engagement rate: {engagement}
        current comments: {self.commented} | current interactions: {self.interacted}
        current likes: {self.liked} | current skips: {self.skipped}"""

        return summary

    # for internal use to print out class state
    def summary(self):
        # define engagement rate (handle zero division)
        try:
            engagement = round(self.liked / (self.liked + self.skipped), 3)
        except ZeroDivisionError:
            engagement = -1

        e_time = round(time() - self.start_time, 2)

        # print out a summary of the current running state in console
        summary = f"""
        elapsed time: {e_time}s | total likes: {self.likes} | engagement rate: {engagement}
        current comments: {self.commented} | current interactions: {self.interacted}
        current likes: {self.liked} | current skips: {self.skipped}"""

        print(summary)

    # Utility methods for setting variables
    def set_like(low:int, high:int):
        self.like_prob = (low, high)
        
    def set_interact(toggle:bool, low:int, high:int):
        self.interact = toggle
        self.interact_prob = (low, high)

    def set_comment(toggle:bool, low:int, high:int):
        self.comment = toggle
        self.comment_prob = (low, high)

    
    def like(self):
        """
        like a photo and go to the next one with prob% chance
        """
        prob = random.randint(self.like_prob[0], self.like_prob[1])
        # %prob chance excute the function
        if random.randrange(1, 100) <= prob:
            # double click to like
            ahk.mouse_move(1500, 1000, speed=10, blocking=True)
            ahk.double_click()
            self.rsleep(4)

            # certain chance to comment
            self.comment()

            # certain chance to interact with user profile
            self.interact()

            # update the tracker
            self.liked +=1
        else:
            self.skipped +=1

        if self.liked >= self.likes:
            self.terminate = True
            return

        # click next arrow icon
        ahk.mouse_move(2675, 943, speed=10, blocking=True)
        ahk.click()
        self.rsleep(4)

        # Personal preference: bare return
        return # explicit approach: return None


    def interact(self, low:int = 1, high:int = 3):
        """
        click into a user profile and randomly like %low-%high posts among the first 12 posts
        prob: % of chance to interact (e.g. 10 means there's 10% of chance to interact)
        low: lower bound of # of posts will interact with
        high: upper bound of # of posts will interact with
        """
        prob = random.randint(self.interact_prob[0], self.interact_prob[1])
        # %prob chance excute the function
        if random.randint(1,100) <= prob:
            # ctrl + click on the user profile link in a new tab (important otherwise hard to return back to initial carousel)
            ahk.mouse_move(2010, 561, speed=10, blocking=True)
            ahk.key_down('control') # press down ctrl
            ahk.click() # click
            ahk.key_up('control') # release the key
            self.rsleep(3)

            # click into the newly opened tab
            ahk.mouse_move(1900, 50, speed=10, blocking=True)
            ahk.click()
            self.rsleep(3)

            # press page down to get the first 12 posts
            ahk.key_press('pgdn')

            # randomly like low-high posts
            interact_goal = random.randint(low, high)
            post_coords = random.sample(user_profile_coords, interact_goal) # return a list of randomly picked coords
            for (x, y) in post_coords:
                # click on the post
                ahk.mouse_move(x, y, speed=10, blocking=True)
                ahk.click()
                self.rsleep(3)

                # double click to like
                ahk.mouse_move(1500, 1000, speed=10, blocking=True)
                ahk.double_click()
                self.rsleep(4)

                # close tab
                ahk.mouse_move(2666, 228, speed=10, blocking=True)
                ahk.double_click()
                self.rsleep(2)

            # when finishing interacting, close the tab by pressing ctrl + w
            ahk.key_down('control')
            ahk.key_press('w')

            self.interacted += 1
            
        return # return to like()


    def comment(self):
        prob = random.randint(self.comment_prob[0], self.comment_prob[1])
        # %prob chance excute the function
        if random.randint(1, 100) <= prob:
            # click on the comment entry
            ahk.mouse_move(2152, 1356, speed=10, blocking=True)
            ahk.click()
            self.rsleep(1)

            # randomly commenting + random sleep to simulate typing
            ahk.type(comments[randint(0, len(comments) - 1)])
            self.rsleep(6)

            # press enter to send
            ahk.key_press('enter')
            self.rsleep(2)

            self.commented += 1

        return # return to like()


    def rsleep(self, sec:int):
        """randomly sleep b/w 70% - 100% seconds"""
        sleep(sec * np.random.uniform(low=0.5, high=1.5))
        # implicit return: this method acctually returns None


    def run(self):
        while not self.terminate:
            self.summary()
            self.like() # internal randomization
        return


if __name__ == '__main__':
    adam = Adam(likes=5, random_offset=True)
    adam.set_interact(True, 10, 20)
    adam.set_comment(True, 5, 10)
    adam.run()

        
    
    