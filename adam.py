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
        u'Awesome post :))',
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
        u'Great content!!',
        u'awesome content!!!',
        u'Awesome content!!',
        u'100/100 love it!',
        u'This is just incredible :^)',
        u'amazing shot!']

hashtags = ['#landscapepainting',
        '#landscapelovers',
        '#landscapephotography',
        '#artstation']

# the screen coordinates after
user_profile_coords=[
    # (1400, 400), # comment out the 1st one which will be liked already
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

# browse result page top 6 coords
brp_coords = [
    (1400, 1000),
    (1400, 1700),
    (1900, 1000),
    (1900, 1700),
    (2400, 1000),
    (2400, 1700),
]

# other coordinates for the script
image_coord = (1500, 1000)
like_coord = (1850, 1130)
comment_text_field_coord = (2152, 1356)
story_icon_coord = (1430, 450)
next_icon_coord = (2675, 943)
user_name_coord = (2010, 561)
new_tab_coord = (1900, 50)
rand_profile_coord = (2600, 600)
ins_post_cross_coord = (2666, 228)
chrome_tab_cross_coord = (2117, 60)
search_field_coord = (1660, 220)
first_hashtag_coord = (1800, 375)

ahk = AHK()

# OOP Review:
# class is a blueprint and an instance is an ovject that is built from a class and contains real data
class Adam():
    # note: every function inside a class is called a "instance method"
    def __init__(self, likes:int = 20, random_offset_yn:bool = True, hp_interaction:bool = False):
        """
        Instance Attributes:
            likes: total likes you want to engage including profile interaction if it's set to True
            interact: set to False by default. Will randomly interact with user profile if it's set to True
            comment: set to False by default. Will randomly comment liked posts if it's set to True
            random_offset_yn: randomly deflate likes within its 60% - 100%
        """
        if random_offset_yn:
            self.likes = int(likes * np.random.uniform(low=0.6, high=1.0))
        else:
            self.likes = likes
        self.interact_yn = False
        self.comment_yn = False
        self.random_offset_yn = random_offset_yn
        self.hp_interaction = hp_interaction

        # internal trackers
        self.liked = 0
        self.skipped = 0
        self.interacted = 0
        self.commented = 0
        self.start_time = time()
        self.interacting = False
        self.terminate = False

        # default randomization (default interval that reset everytime the function is called)
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

        e_time = round(time() - self.start_time, 0)

        # print out a summary of the current running state in console
        summary = f"""
        e_time: {e_time}s | goal: {self.likes} likes | engagement: {engagement}
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

        e_time = round(time() - self.start_time, 0)

        # print out a summary of the current running state in console
        summary = f"""
        e_time: {e_time}s | goal: {self.likes} likes | engagement: {engagement}
        current comments: {self.commented} | current interactions: {self.interacted}
        current likes: {self.liked} | current skips: {self.skipped}"""

        print(summary)

    # Utility methods for setting variables
    def set_like(self, low:int, high:int):
        self.like_prob = (low, high)
        
    def set_interact(self, toggle:bool, low:int, high:int):
        self.interact_yn = toggle
        self.interact_prob = (low, high)

    def set_comment(self, toggle:bool, low:int, high:int):
        self.comment_yn = toggle
        self.comment_prob = (low, high)

    
    def like(self):
        """
        like a photo and go to the next one with prob% chance
        """
        prob = random.randint(self.like_prob[0], self.like_prob[1])
        # %prob chance excute the function
        if random.randrange(1, 100) <= prob:
            # double click to like
            ahk.mouse_move(*like_coord, speed=10, blocking=True)
            ahk.click()
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
            self.summary()
            print('Reached goal. Terminating ...')
            return

        # click next arrow icon
        ahk.mouse_move(*next_icon_coord, speed=10, blocking=True)
        ahk.click()
        self.summary()
        self.rsleep(8)

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
            ahk.mouse_move(*user_name_coord, speed=10, blocking=True)
            ahk.key_down('control') # press down ctrl
            ahk.click() # click
            ahk.key_up('control') # release the key
            self.rsleep(20)

            # click into the newly opened tab
            ahk.mouse_move(*new_tab_coord, speed=10, blocking=True)
            ahk.click()
            self.rsleep(3)

            # press page down to get the first 12 posts
            # ahk.mouse_move(*rand_profile_coord, speed=10, blocking=True)
            # ahk.click()
            ahk.key_press('pgdn')
            self.rsleep(1)

            # randomly like low-high posts
            interact_goal = random.randint(low, high)
            post_coords = random.sample(user_profile_coords, interact_goal) # return a list of randomly picked coords
            for (x, y) in post_coords:
                # click on the post
                ahk.mouse_move(x, y, speed=10, blocking=True)
                ahk.click()
                self.rsleep(3)

                # double click to like
                ahk.mouse_move(*like_coord, speed=10, blocking=True)
                ahk.click()
                self.rsleep(4)

                # close instagram post tab
                ahk.mouse_move(*ins_post_cross_coord, speed=10, blocking=True)
                ahk.click()
                self.rsleep(2)

            # when finishing interacting, close the tab by pressing ctrl + w (bug exists)
            ahk.mouse_move(*chrome_tab_cross_coord, speed=10, blocking=True)
            ahk.click()
            self.rsleep(1)

            self.interacted += 1
            self.liked += interact_goal
            
        return # return to like()


    def comment(self):
        prob = random.randint(self.comment_prob[0], self.comment_prob[1])
        # %prob chance excute the function
        if random.randint(1, 100) <= prob:
            # click on the comment entry
            ahk.mouse_move(*comment_text_field_coord, speed=10, blocking=True)
            ahk.click()
            self.rsleep(1)

            # randomly commenting + random sleep to simulate typing
            ahk.type(comments[random.randint(0, len(comments) - 1)])
            self.rsleep(6)

            # press enter to send
            ahk.key_press('enter')
            self.rsleep(2)

            self.commented += 1

        return # return to like()


    def rsleep(self, sec:int):
        """randomly sleep b/w 50% - 150% seconds"""
        sleep(sec * np.random.uniform(low=0.5, high=1.5))
        # implicit return: this method acctually returns None


    def run(self):
        ## logging into instagram
        # click on the chrome icon
        # ahk.mouse_move(2152, 1356, speed=10, blocking=True)
        # ahk.click()
        # self.rsleep(1)

        ## random Homepage interactions
        # check out some stories (click on the 1st story and randomly browse x stories)
        if self.hp_interaction:
            ahk.mouse_move(*story_icon_coord, speed=10, blocking=True)
            ahk.click()
            self.rsleep(3)
            for i in range(random.randint(1, 12)):
                ahk.key_press('right')
                self.rsleep(4)

            # close the instagram story
            ahk.mouse_move(*ins_post_cross_coord, speed=10, blocking=True)
            ahk.click()
            self.rsleep(2)

            # click on the search field
            ahk.mouse_move(*search_field_coord, speed=10, blocking=True)
            ahk.click()
            self.rsleep(2)

            # randomly picked one hashtag and search it
            hashtag = hashtags[random.randint(0, len(hashtags) - 1)]
            print(f'chosen hashtag: {hashtag}')
            ahk.type(hashtag)
            self.rsleep(8)

            # press enter to search
            ahk.key_press('enter')
            self.rsleep(4)

            # Randomly click one of the first 6 posts in "Top posts" to start
            brp_coord = brp_coords[random.randint(0, len(brp_coords) - 1)]
            ahk.mouse_move(*brp_coord, speed=10, blocking=True)
            ahk.click()
            self.rsleep(3)

        ## main code for engaging users
        while not self.terminate:
            self.like() # internal randomization
        self.rsleep(10)

        ## add closing the window after finish the session
        win = ahk.active_window
        win.kill()

        return


if __name__ == '__main__':
    adam = Adam(likes=25, random_offset_yn=True, hp_interaction=False)
    adam.set_like(50, 80)
    adam.set_interact(True, 10, 20)
    # adam.set_interact(True, 100, 100)
    adam.set_comment(True, 1, 1)
    # adam.set_comment(True, 100, 100)
    adam.run()

        
    
    