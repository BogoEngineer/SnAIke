import random
import math
random.seed()


class Ground:
    def __init__(self, height, width):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        #self. fruit = [random.randint(self.x, self.x+self.width-1), random.randint(self.y, self.y+self.height-1)] #x,y coordinates

        self.fruit = [random.randint(self.x, self.x + self.width - 2), random.randint(self.y, self.y + self.height - 2)]

    def generateFruit(self):
        self.fruit =  [random.randint(self.x, self.x+self.width-2), random.randint(self.y, self.y+self.height-2)]



class Snake:
    id = 0;
    def __init__(self, xHead, yHead):
        Snake.id+=1
        self.hungry_for = 0 #for how many time units snake hasnt eat
        self.id = Snake.id
        #self.speedX = 2.5
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
        if self.body[0][0] < ground.x:
            self.body[0][0] += ground.width
        if self.body[0][0]>(ground.x + ground.width):
            self.body[0][0] -= ground.width
        if self.body[0][1] < ground.y:
            self.body[0][1] += ground.height
        if self.body[0][1] > (ground.y + ground.height):
            self.body[0][1] -= ground.height
        return False


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
        if (self.body[0][0] == ground.fruit[0] or self.body[0][0] == ground.fruit[0] + 1) and (self.body[0][1] == ground.fruit[1] or self.body[0][1] == ground.fruit[1]+1):
            if(len(self.body) == 1):
                self.body.append([self.body[0][0] - self.speedX, self.body[0][1] - self.speedY])
            elif(self.body[-2][0] == self.body[-1][0]):
                self.body.append([self.body[-1][0], self.body[-1][1]-self.body[-2][1] + self.body[-1][1]])
            elif(self.body[-2][1] == self.body[-2][1]):
                self.body.append([self.body[-1][0], self.body[-2][1] - self.body[-1][1] + self.body[-1][1]])
            self.score += 1
            self.hungry_for = 0
            ground.generateFruit()
            return True
        self.hungry_for += 1
        return False

    def distance(self, ground):
        x1 = self.body[0][0]
        y1 = self.body[0][1]
        x2 = ground.fruit[0]
        y2 = ground.fruit[1]

        return math.sqrt((x1-x2)**2 + (y1-y2)**2)