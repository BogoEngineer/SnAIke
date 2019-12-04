import random

random.seed()


class Ground:
    def __init__(self, height, width):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self. fruit = [random.randint(self.x, self.x+self.width-1), random.randint(self.y, self.y+self.height-1)]

    def generateFruit(self):
        self.fruit =  [random.randint(self.x, self.x+self.width-1), random.randint(self.y, self.y+self.height-1)]



class Snake:
    def __init__(self, xHead, yHead):
        self.speedX = 1
        self.speedY = 0
        self.body = [[xHead, yHead]]
        self.score = 1

    def move(self, ground):
        if(len(self.body) == 1):
            self.body[0][0] += self.speedX
            self.body[0][1] += self.speedY
            if (self.wallCrashed(ground) or self.raveled()):
                return False
            else:
                return True
        if(len(self.body) == 2):
            self.body[1][0] = self.body[0][0]
            self.body[1][1] = self.body[0][1]
            self.body[0][0] += self.speedX
            self.body[0][1] += self.speedY
            if (self.wallCrashed(ground) or self.raveled()):
                return False
            else:
                return True
        newBody = [[0,0]]
        for i, part in enumerate(self.body):
            if not i == len(self.body)-1: newBody.append(part)
        newBody[0] = [newBody[1][0]+self.speedX, newBody[1][1]+self.speedY]
        self.body = newBody
        if(self.wallCrashed(ground) or self.raveled()):
            return False
        else: return True

    def wallCrashed(self, ground):
        if(self.body[0][0] < ground.x or self.body[0][0]>(ground.x + ground.width) or self.body[0][1] < ground.y or self.body[0][1] > (ground.y + ground.height)):
            return True
        else: return False

    def raveled(self):
        for i, part in enumerate(self.body):
            if (not i == 0) and self.body[0] == part:
                return True
        return False

    #wicked snake
    """
    def eat(self, ground):
        if(self.body[0][0] == ground.fruit[0] and self.body[0][1] == ground.fruit[1]):
            self.body.append([self.body[-1][0]-self.speedX, self.body[-1][1]+self.speedY])
            ground.generateFruit()
            return True
        else: return False
    """

    def eat(self, ground):
        if (self.body[0][0] == ground.fruit[0] and self.body[0][1] == ground.fruit[1]):
            if(len(self.body) == 1):
                self.body.append([self.body[0][0] - self.speedX, self.body[0][1] - self.speedY])
            elif(self.body[-2][0] == self.body[-1][0]):
                self.body.append([self.body[-1][0], self.body[-1][1]-self.body[-2][1] + self.body[-1][1]])
            elif(self.body[-2][1] == self.body[-2][1]):
                self.body.append([self.body[-1][0], self.body[-2][1] - self.body[-1][1] + self.body[-1][1]])
            self.score += 1
            ground.generateFruit()
            return True
        return False