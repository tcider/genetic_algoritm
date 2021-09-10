from random import randint, shuffle, sample
import matplotlib.pyplot as plt
import time

# Параметры генетического алгоритма, SELECTION_SIZE четное, MUTATIONS меньше числа вещей

class Element:
    """Класс особи популяции"""
    # Список для "хромосомы"
    gens = []
    # Длина хромосомы
    size = 0
    # Ценность особи - уроень жизнеспособности
    total_cost = 0
    # Вес/размер/себестоимость особи
    total_weight = 0
    # Флаг отбора в селекции
    selected = 0

    def __init__(self, items, bag_size):
        while True:
            self.gens = [randint(0, 1) for i in range(len(items))]
            self.count_params(items)
            if self.total_weight <= bag_size:
                break
        self.size = len(items)

    def count_params(self, items):
        self.total_weight = 0
        self.total_cost = 0
        for i in range(self.size):
            self.total_weight += items[i][0] * self.gens[i]
            self.total_cost += items[i][1] * self.gens[i]


class Population:
    """Класс популяции - содержит список особей"""
    items = []
    bag_size = 0
    size = 0
    elem_size = 0
    parents = []
    children = []
    best_gens = []
    best_cost = 0
    counter = 0

    def __init__(self, items, bag_size):
        for _ in range(POPULATION_SIZE):
            self.parents.append(Element(items, bag_size))
        self.size = POPULATION_SIZE
        self.bag_size = bag_size
        self.elem_size = self.parents[0].size
        self.items = items

    def make_selection(self):
        """Селекцию выбираем с вероятностью пропорциональной приспособленности особи"""
        selected_list = []
        max_cost = 0
        # Считаем максимально возможную ценность для селекции
        for item in self.items:
            max_cost += item[1]
        while len(selected_list) < SELECTION_SIZE:
            i = randint(0, self.size - 1)
            if not self.parents[i].selected and randint(0, max_cost) <= self.parents[i].total_cost:
                self.parents[i].selected = 1
                selected_list.append(self.parents[i])
        self.parents = selected_list
        self.size = SELECTION_SIZE

    def copy_element(self, element):
        res = Element(self.items, self.bag_size)
        for i in range(element.size):
            res.gens[i] = element.gens[i]
        res.total_weight = element.total_weight
        res.total_cost = element.total_cost
        return res

    def mutations(self):
        mut_num = MUTATIONS
        if mut_num > self.elem_size:
            mut_num = self.elem_size
        for child in self.children:
            new_gens = []
            for i in child.gens:
                new_gens.append(i)
            gen_list = sample(range(0, child.size), mut_num)
            for i in gen_list:
                if new_gens[i]:
                    new_gens[i] = 0
                else:
                    new_gens[i] = 1
            weight = 0
            cost = 0
            for i in range(child.size):
                weight += self.items[i][0] * new_gens[i]
                cost += self.items[i][1] * new_gens[i]
            if weight <= self.bag_size and cost > child.total_cost:
                child.gens = new_gens
                child.count_params(self.items)
            self.counter += 1

    def crossover(self):
        children = []
        i = 0
        while i < self.size - 1:
            # Точка скрещивания вычисляется рандомно
            cross_pnt = randint(0, self.elem_size - 1)
            child_a = self.copy_element(self.parents[i])
            child_b = self.copy_element(self.parents[i + 1])
            tmp = child_a.gens[cross_pnt]
            child_a.gens[cross_pnt] = child_b.gens[cross_pnt]
            child_b.gens[cross_pnt] = tmp
            child_a.count_params(self.items)
            if child_a.total_weight <= self.bag_size:
                children.append(child_a)
            child_b.count_params(self.items)
            if child_b.total_weight <= self.bag_size:
                children.append(child_b)
            i += 2
            self.counter += 1
            MUT.append(child_b.total_cost)
        self.children = children

    def make_new_age(self):
        new_population = []
        self.children.sort(key=lambda x: x.total_cost, reverse=True)
        self.parents.sort(key=lambda x: x.total_cost, reverse=True)
        i = 0
        while i < min(int(SELECTION_SIZE / 2) + 1, len(self.children)):
            new_population.append(self.children[i])
            i += 1
        i = 0
        while len(new_population) < SELECTION_SIZE:
            new_population.append(self.parents[i])
            i += 1
        new_population.sort(key=lambda x: x.total_cost, reverse=True)
        self.best_gens = new_population[0].gens
        self.best_cost = new_population[0].total_cost
        shuffle(new_population)
        self.parents = new_population


# items: List[Tuple[weight: int, cost: int]], bag_size: int
def solve(items, bag_size):
    population = Population(items, bag_size)
    population.make_selection()
    no_result_iter = 0
    result = []
    result_cost = 0
    while no_result_iter < AGES_WO_EVOLUTION:
        population.crossover()
        population.mutations()
        population.make_new_age()
        if population.best_cost > result_cost:
            result = population.best_gens
            result_cost = population.best_cost
        else:
            no_result_iter += 1
        ITER_AGE.append(population.counter)
        COST.append(result_cost)
    return result, result_cost

params = []
with open('params.txt', 'r') as tmp_file:
    for line in tmp_file.readlines():
        tpl = line.split()
        tpl[1] = int(tpl[1])
        params.append(tpl[1])
POPULATION_SIZE = params[0]
SELECTION_SIZE = params[1]
AGES_WO_EVOLUTION = params[2]
MUTATIONS = params[3]
items = []
with open('items.txt', 'r') as tmp_file:
    for line in tmp_file.readlines():
        tpl = line.split()
        tpl[0] = int(tpl[0])
        tpl[1] = int(tpl[1])
        items.append(tpl)
bag_size = int(input("Введите обьем рюкзака - "))

ITER_AGE = []
COST = []
TIME = []
MUT = []

res, res_cost = solve(items, bag_size)

for i in range(len(items)):
    print("Вещь №" + str(i + 1), end="")
    if not res or not res[i]:
        print(" не", end="")
    print(" берем.")

plt.figure(figsize=(10,20))

plt.subplot(3, 1, 1)
plt.plot(ITER_AGE, color = 'teal', marker = '^')
plt.title("Колличество итераций на каждой эпохе", fontsize=14)
plt.xlabel('Эпоха', fontsize=10, color='green')
plt.ylabel('Коллчичестов итераций', fontsize=10, color='green')
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(COST, color = 'steelblue', marker = 'X')
plt.title("Ценность рюкзака на каждой эпохе", fontsize=14)
plt.xlabel('Эпоха', fontsize=10, color='blue')
plt.ylabel('Ценность рюкзака', fontsize=10, color='blue')
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(MUT, color = 'seagreen')
plt.title("Разброс ценности рюкзака на каждом скрещивании", fontsize=14)
plt.xlabel('Скрещивание №', fontsize=10, color='green')
plt.ylabel('Ценность рюкзака', fontsize=10, color='green')
plt.grid(True)

plt.subplots_adjust(hspace=0.5)

plt.show()