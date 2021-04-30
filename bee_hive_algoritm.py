from random import randint


class ScoutBee: # Класс для пчелы Разведчика
    vector = [] # бинарная маска выбранных предметов
    size = 0 # макс размер вектора
    honey = 0 # ценнсоть выбранных предметов
    weight = 0 # обьем выбранных предметов

    def __init__(self, items, bag_size): # Создаем медоноса "рандомно"
        while True:
            self.vector = [randint(0, 1) for i in range(len(items))]
            self.count_bee(items)
            if self.weight <= bag_size:
                break
        self.size = len(items)

    def count_bee(self, items): # Считаем вес и ценность Медоноса
        self.weight = 0
        self.honey = 0
        for i in range(self.size):
            self.weight += items[i][0] * self.vector[i]
            self.honey += items[i][1] * self.vector[i]


class BeeHive:
    hive = [] # Список для хранения всех пчел улья
    items = [] # изначально заданный 2х мерный массив обьемов и весов
    bag_size = 0 # размер рюкзака
    scout_size = 0 # Входной параметр - сколько пчел разведичков
    honey_size = 0 # Входн параметр - сколько пчел медоносов
    hamming_distance = 0 # Входн параметр - расстояние Хемминга
    random_size = 0 # Сколько новых "рнадомных чел" добавлять для обновления улья
    bee_size = 0 # размер вектора одной пчелы
    best_bee = [] # вектор лучшей пчелы в улье
    best_honey = 0 # ценность лучшей пчелы в улье

    def __init__(self, items, params, bag_size):
        self.scout_size = params[0]
        self.honey_size = params[1]
        self.hamming_distance = params[2]
        self.random_size = params[3]
        self.bag_size = bag_size
        self.bee_size = len(items)
        self.items = items
        for _ in range(self.scout_size):
            self.hive.append(ScoutBee(items, bag_size))


    def local_search(self, scout_bee_index): # Создаем окрестность пчелы развечика в honey_size кол-ве пчел медоносов
        first_vector = self.hive[scout_bee_index].vector.copy()
        for _ in range(self.honey_size):
            bee_vector = first_vector.copy()
            for _ in range(self.hamming_distance):
                i = randint(0, self.bee_size - 1)
                bee_vector[i] = 0 if bee_vector[i] else 1
            weight = 0
            cost = 0
            for i in range(self.bee_size):
                weight += self.items[i][0] * bee_vector[i]
                cost += self.items[i][1] * bee_vector[i]
            if weight <= self.bag_size and cost > self.hive[scout_bee_index].honey:
                self.hive[scout_bee_index].vector = bee_vector
                self.hive[scout_bee_index].count_bee(self.items)

    def sub_totals(self): # Вычислем лучшую пчелу и обновлем random_size худших
        self.hive.sort(key=lambda x: x.honey, reverse=True)
        self.best_bee = self.hive[0].vector
        self.best_honey = self.hive[0].honey
        for i in range(self.random_size):
            self.hive[self.scout_size - 1 - i] = ScoutBee(self.items, self.bag_size)


def main():
    items = []
    params = []
    with open('items.txt', 'r') as tmp_file:
        for line in tmp_file.readlines():
            tpl = line.split()
            tpl[0] = int(tpl[0])
            tpl[1] = int(tpl[1])
            items.append(tpl)
    with open('params.txt', 'r') as tmp_file:
        for line in tmp_file.readlines():
            tpl = line.split()
            tpl[1] = int(tpl[1])
            params.append(tpl[1])
    bag_size = int(input("Введите обьем рюкзака - "))

    beehive = BeeHive(items, params, bag_size)
    idle_i = 0
    max_honey = 0
    result = []
    while idle_i < params[4]:
        for i in range(params[0]):
            beehive.local_search(i)
        beehive.sub_totals()
        if beehive.best_honey > max_honey:
            result = beehive.best_bee
            max_honey = beehive.best_honey
        else:
            idle_i += 1

    for i in range(len(items)):
        print("Вещь №" + str(i + 1) + "(вес-" + str(items[i][0]) + ", цена-" + str(items[i][1]) + ")", end="")
        if not result or not result[i]:
            print(" не", end="")
        print(" берем.")


if __name__ == "__main__":
    main()
