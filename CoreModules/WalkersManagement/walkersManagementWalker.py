import random


class Walker:
    def __init__(self, cell_i, cell_j, house):
        self.head = None
        self.cell_i = cell_i
        self.cell_j = cell_j
        self.house = house
        self.direction = list()

    def walk(self, road_layer):
        right = "right"
        left = "left"
        up = "up"
        down = "down"
        ran = 0
        self.direction.clear()

        r = (self.cell_i, self.cell_j + 1)
        le = (self.cell_i, self.cell_j - 1)
        u = (self.cell_i + 1, self.cell_j)
        d = (self.cell_i - 1, self.cell_j)

        if (road_layer.array[r[0]][r[1]]).dic["version"] != "null":
            rr = True
        if (road_layer.array[le[0]][le[1]]).dic["version"] != "null":
           ll = True
        if (road_layer.array[u[0]][u[1]]).dic["version"] != "null":
            uu = True
        if (road_layer.array[d[0]][d[1]]).dic["version"] != "null":
            dd = True

        if self.head == right:
            if not (rr or dd or uu):
                self.direction.append(left)
            else:
                if rr:
                    self.direction.append(right)
                if uu:
                    self.direction.append(up)
                if dd:
                    self.direction.append(down)
        elif self.head == up:
            if not (rr or ll or uu):
                self.direction.append(down)
            else:
                if rr:
                    self.direction.append(right)
                if uu:
                    self.direction.append(up)
                if ll:
                    self.direction.append(left)
        elif self.head == left:
            if not (ll or dd or uu):
                self.direction.append(right)
            else:
                if ll:
                    self.direction.append(left)
                if uu:
                    self.direction.append(up)
                if dd:
                    self.direction.append(down)
        elif self.head == down:
            if not (rr or dd or ll):
                self.direction.append(up)
            else:
                if rr:
                    self.direction.append(right)
                if ll:
                    self.direction.append(left)
                if dd:
                    self.direction.append(down)

        ran = random.randint(0, len(self.direction))
        if self.direction[ran - 1] == right:
            self.cell_i += 1
            self.head = right
        elif self.direction[ran - 1] == left:
            self.cell_i -= 1
            self.head = left
        elif self.direction[ran - 1] == up:
            self.cell_j += 1
            self.head = up
        elif self.direction[ran - 1] == down:
            self.cell_j -= 1
            self.head = down

    def work(self):
        pass


class Engineer(Walker):
    def work(self):
        pass


class Prefect(Walker):
    def work(self):
        pass


class Immigrant(Walker):
    def find_house(self):
        # Parcourir la liste des maisons, trouver celle dans lesquelle peut s'installer(nombre d'habitant, niveau d'habitaion)
        pass


class Cart_Pusher(Walker):
    def work(self):
        pass


class Delivery_Boy(Walker):
    def work(self):
        pass


class Market_Trader(Walker):
    def work(self):
        pass