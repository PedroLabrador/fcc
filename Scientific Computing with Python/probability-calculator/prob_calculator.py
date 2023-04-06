import copy
import random
# Consider using the modules imported above.

class Hat:
    def __init__(self, **kwargs):
        self.contents = []

        for key, value in kwargs.items():
            for i in range(value):
                self.contents.append(key)

    def draw(self, num):
        to_remove = []
        if num > len(self.contents):
            return self.contents
        for i in range(num):
            random_index = random.randint(0, len(self.contents) - 1)
            to_remove.append(self.contents[random_index])
            self.contents.pop(random_index)
        return to_remove
        

def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    found = 0
    for i in range(num_experiments):
        copied_hat = copy.deepcopy(hat)
        drawed = copied_hat.draw(num_balls_drawn)
        drawed_dict = {}
        for ball in drawed:
            try:
                drawed_dict[ball] += 1
            except:
                drawed_dict[ball] = 1

        success = True
        for ball_key_expected, ball_val_expected in expected_balls.items():
            ball_drawed = drawed_dict.get(ball_key_expected)
            if not (ball_drawed and ball_drawed >= ball_val_expected):
                success = False
                break

        if success:
            found += 1

    return found / num_experiments
