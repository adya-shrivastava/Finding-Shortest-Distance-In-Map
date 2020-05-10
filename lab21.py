import math
import heapq
import sys
from PIL import Image

# from _collections import deque

X_VALUE = 10.29
Y_VALUE = 7.55
UPHILL_FACTOR = 0.5
DOWNHILL_FACTOR = 1.25


class Terrain:
    __slots__ = "terrain_image", "elevation_file", "path_file", "output_image_filename", "season", "terrain_legend", \
                "pixel_values", "elevation_list", "path", "total_distance"

    def __init__(self, terrain_image, elevation_file, path_file, season, output_image_filename):
        self.path = []
        self.terrain_image = terrain_image
        self.elevation_file = elevation_file
        self.path_file = path_file
        self.output_image_filename = output_image_filename
        self.season = season
        self.terrain_legend = {}
        self.pixel_values = []
        self.elevation_list = []
        self.total_distance = 0

    def set_terrain_legend(self):
        if self.season == "summer":
            self.terrain_legend = {'#F89412': ("Open land", 1.5),
                                   '#FFC000': ("Rough meadow", 0.8),
                                   '#FFFFFF': ("Easy movement forest", 2.0),
                                   '#02D03C': ("Slow run forest", 0.85),
                                   '#028828': ("Walk forest", 0.7),
                                   '#054918': ("Impassible vegetation", 0.1),
                                   '#0000FF': ("Lake/Swamp/Marsh", 0.000001),
                                   '#473303': ("Paved road", 1.7),
                                   '#000000': ("Footpath", 1.8),
                                   '#CD0065': ("Out of bounds", 0)}
        elif self.season == "fall":
            self.terrain_legend = {'#F89412': ("Open land", 1.5),
                                   '#FFC000': ("Rough meadow", 0.8),
                                   '#FFFFFF': ("Easy movement forest", 1.0),
                                   '#02D03C': ("Slow run forest", 0.85),
                                   '#028828': ("Walk forest", 0.7),
                                   '#054918': ("Impassible vegetation", 0.1),
                                   '#0000FF': ("Lake/Swamp/Marsh", 0.000001),
                                   '#473303': ("Paved road", 1.7),
                                   '#000000': ("Footpath", 1.8),
                                   '#CD0065': ("Out of bounds", 0)}
        elif self.season == "winter":
            self.color_winter()
        else:
            pass

    def get_terrain_speed(self, terrain):
        return self.terrain_legend[terrain][1]

    def get_pixel_values(self):
        im = Image.open(self.terrain_image, "r")
        # pix_val = list(im.getdata())
        # # print(len(pix_val))
        # print(pix_val)
        # self.pixel_values = [[None for j in range(500)] for i in range(395)]
        # for i in range(395):
        #     templist = pix_val[:500]
        #     for j in range(len(templist)):
        #         if i == 100 and j == 230:
        #             print(templist[j])
        #         templist[j] = rgb_to_hex(templist[j][:-1])
        #         if i == 100 and j == 230:
        #             print(templist[j])
        #     self.pixel_values[i] = templist

        # print(len(self.pixel_values), len(self.pixel_values[0]))
        # print(pix_val[100][230])

        pix_val = im.load()
        self.pixel_values = [[None for j in range(500)] for i in range(395)]

        for i in range(395):
            for j in range(500):
                self.pixel_values[i][j] = rgb_to_hex(pix_val[i, j][:-1])

        # print(self.pixel_values[100][230])

    def get_elevation_list(self):
        file = open(self.elevation_file, 'r')
        count = 0
        for i in file:
            x = str(i).split()
            self.elevation_list.append(x[:-5])
            # print(len(x), x)
            count += 1
        self.elevation_list = [[self.elevation_list[j][i] for j in range(len(self.elevation_list))] for i in
                               range(len(self.elevation_list[0]))]

        print(len(self.elevation_list), len(self.elevation_list[0]))

    def calculate_distance(self, src, dest):

        # print("\t\t in calculate distance", src, dest)
        x1, y1 = src
        x2, y2 = dest
        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)
        return math.sqrt(pow((x2 - x1) * X_VALUE, 2) + pow((y2 - y1) * Y_VALUE, 2) +
                         pow(float(self.elevation_list[x1][y1]) - float(self.elevation_list[x2][y2]), 2))

    def calculate_heuristic(self, src, dest):
        # print(src[0], src[1])
        # print(self.pixel_values[src[0]][src[1]])
        speed = self.get_terrain_speed('#F89412')

        # if float(self.elevation_list[dest[0]][dest[1]]) - float(self.elevation_list[src[0]][src[1]]) < 0:
        #     speed = speed * DOWNHILL_FACTOR
        # else:
        #     speed = speed * UPHILL_FACTOR
        return self.calculate_distance(src, dest) / speed

    # def calculate_cost_from_source(self, src, dest):
    #     distance = self.calculate_distance(src, dest)
    #     speed = self.get_terrain_speed(self.pixel_values[dest[0]][dest[1]])
    #
    #     if float(self.elevation_list[dest[0]][dest[1]]) - float(self.elevation_list[src[0]][src[1]]) < 0:
    #         speed = speed * DOWNHILL_FACTOR
    #     else:
    #         speed = speed * UPHILL_FACTOR
    #     # print()
    #     # try:
    #     return distance / speed
    #     # except ZeroDivisionError as e:
    #     #     print("division by zero error", dest[0], dest[1], src[0], src[1])

    def calculate_speed(self, src, dest):
        speed = self.get_terrain_speed(self.pixel_values[dest[0]][dest[1]])
        # elevation = float(self.elevation_list[dest[0]][dest[1]]) - float(self.elevation_list[src[0]][src[1]]) * -1
        tan_val = (float(self.elevation_list[dest[0]][dest[1]]) - float(self.elevation_list[src[0]][src[1]])) / (self.calculate_distance(src, dest))

        if float(self.elevation_list[dest[0]][dest[1]]) - float(self.elevation_list[src[0]][src[1]]) < 0:
            speed = speed * DOWNHILL_FACTOR * (1 - tan_val)
        elif float(self.elevation_list[dest[0]][dest[1]]) - float(self.elevation_list[src[0]][src[1]]) > 0:
            speed = speed * UPHILL_FACTOR * (1 - tan_val)

        return speed

    def reachable(self, current):
        # if self.season != "winter":
        #     return self.pixel_values[current[0]][current[1]] != '#0000FF'
        # print(self.pixel_values[current[0]][current[1]])
        return self.pixel_values[current[0]][current[1]] != '#CD0065' and self.pixel_values[current[0]][current[1]] != '#0000FF'

    def neighbors(self, current):
        # print("\tin neighbors", current)
        i, j = current
        neighbor_list = []
        if i - 1 >= 0 and j - 1 >= 0 and self.reachable((i - 1, j - 1)):
            neighbor_list.append((i - 1, j - 1))
        if i - 1 >= 0 and j >= 0 and self.reachable((i - 1, j)):
            neighbor_list.append((i - 1, j))
        if i - 1 >= 0 and j + 1 < 500 and self.reachable((i - 1, j + 1)):
            neighbor_list.append((i - 1, j + 1))
        if i >= 0 and j - 1 >= 0 and self.reachable((i, j - 1)):
            neighbor_list.append((i, j - 1))
        if i + 1 < 395 and j - 1 >= 0 and self.reachable((i + 1, j - 1)):
            neighbor_list.append((i + 1, j - 1))
        if i >= 0 and j + 1 < 500 and self.reachable((i, j + 1)):
            neighbor_list.append((i, j + 1))
        if i + 1 < 395 and j + 1 < 500 and self.reachable((i + 1, j + 1)):
            neighbor_list.append((i + 1, j + 1))
        if i + 1 < 395 and j < 500 and self.reachable((i + 1, j)):
            neighbor_list.append((i + 1, j))
        # print("\tneighbor list", neighbor_list)
        return neighbor_list

    def read_file(self):
        file = open(self.path_file)
        file = file.readlines()
        for i in range(len(file) -1):
            src = tuple(int(s) for s in file[i].strip().split(" "))
            dest = tuple(int(s) for s in file[i+1].strip().split(" "))
            # print(src, dest)
            self.a_star(src, dest)
            print(self.total_distance)

    def color_winter(self):
        edges_set = set()
        for i in range(395):
            for j in range(500):
                if self.pixel_values[i][j] == "#0000FF":
                    for neighbor in self.neighbors((i, j)):
                        if self.pixel_values[neighbor[0]][neighbor[1]] != "#0000FF" and neighbor not in edges_set:
                            edges_set.add((neighbor[0], neighbor[1]))

        print(edges_set)




    # def a_star(self, src, dest):
    #
    #     # queue = deque()
    #     # queue.append((0, src))
    #     queue = []
    #     cost = self.calculate_cost_from_source(src, src) + self.calculate_heuristic(src, dest)
    #     # queue.append((cost, src))
    #     visited = {src: [0, None]}
    #     visited_set = set()
    #     heapq.heappush(queue, (cost, src))
    #     visited_set.add(src)
    #     # print(queue.popleft())
    #
    #     while len(queue) > 0:
    #         current = heapq.heappop(queue)
    #         # print(current)
    #
    #         # queue.remove(current)
    #         visited_set.add(current[1])
    #
    #         if current[1] == dest:
    #             break
    #
    #         for neighbor in self.neighbors(current[1]):
    #             cost = self.calculate_cost_from_source(current[1], neighbor) + self.calculate_heuristic(neighbor, dest)
    #             if neighbor not in visited_set:
    #                 if neighbor in visited:
    #                     # print("cost", cost)
    #                     if cost < visited[neighbor][0]:
    #                         # print("in if", cost, visited[neighbor][0], visited[neighbor][1])
    #                         queue.remove((visited[neighbor][0], neighbor))
    #                         # queue.append((cost, neighbor))
    #                         # heapq.heappop(queue)
    #                         heapq.heappush(queue, (cost, neighbor))
    #
    #                         visited[neighbor] = [cost, current[1]]
    #
    #                 else:
    #                     # queue.append((cost, neighbor))
    #                     heapq.heappush(queue, (cost, neighbor))
    #                     visited[neighbor] = [cost, current[1]]
    #
    #                 # visited[neighbor][0] = cost
    #                 # visited[neighbor][1] = current
    #         # print(visited)
    #         # print(queue)
    #     if dest in visited_set:
    #         current = dest
    #         # self.total_distance += visited[current][0]
    #         path = []
    #         while current != src:
    #             path.insert(0, current)
    #             self.total_distance += visited[current][0]
    #             current = visited[current][1]
    #
    #         path.insert(0, src)
    #
    #         self.path.append(path)
    #         print("sdfh",  self.total_distance)
    #         # print("djfbjd", self.path)


    def a_star(self, src, dest):

        # queue = deque()
        # queue.append((0, src))
        queue = []
        cost = 0 + self.calculate_heuristic(src, dest)
        # queue.append((cost, src))
        visited = {src: [0, None, 0]}
        visited_set = set()
        heapq.heappush(queue, (cost, src))
        visited_set.add(src)
        # print(queue.popleft())
        # count = 0
        while len(queue) > 0:
            current = heapq.heappop(queue)
            # print(current)

            # queue.remove(current)
            visited_set.add(current[1])

            if current[1] == dest:
                break

            for neighbor in self.neighbors(current[1]):
                distance = self.calculate_distance(current[1], neighbor)
                speed = self.calculate_speed(current[1], neighbor)
                cost = (distance / speed) + self.calculate_heuristic(neighbor, dest) + current[0]
                if neighbor not in visited_set:
                    # count += 1
                    if neighbor in visited:
                        # print("cost", cost)
                        if cost < visited[neighbor][0]:
                            # print("in if", cost, visited[neighbor][0], visited[neighbor][1])
                            queue.remove((visited[neighbor][0], neighbor))
                            # queue.append((cost, neighbor))
                            # heapq.heappop(queue)
                            heapq.heappush(queue, (cost, neighbor))

                            visited[neighbor] = [cost, current[1], distance]

                    else:
                        # queue.append((cost, neighbor))
                        heapq.heappush(queue, (cost, neighbor))
                        visited[neighbor] = [cost, current[1], distance]

                    # visited[neighbor][0] = cost
                    # visited[neighbor][1] = current
            # print(visited)
            # print(queue)

        # print(visited)

        if dest in visited_set:
            current = dest
            # self.total_distance += visited[current][0]
            path = []
            while current != src:
                path.insert(0, current)
                print(visited[current][2])
                self.total_distance += visited[current][2]
                current = visited[current][1]

            path.insert(0, src)

            self.path.append(path)
            # print("sdfh",  self.total_distance)
            # print("djfbjd", self.path)
            # print(count)

    def output_path(self):
        im = Image.open(self.terrain_image, "r")
        file = im.load()

        self.path = [i for j in self.path for i in j]
        print(len(self.path))
        print(self.total_distance)
        for i in self.path:
            # print(file[i])
            file[i] = (255, 0, 0, 255)

        im.show()


def rgb_to_hex(rgb):
    return '#' + ('%02X%02X%02X' % rgb)


def main():
    terrain = sys.argv[1]
    elevation_file = sys.argv[2]
    path_file = sys.argv[3]
    season = sys.argv[4]
    output_file_name = sys.argv[5]

    t = Terrain(terrain, elevation_file, path_file, season, output_file_name)
    t.get_pixel_values()
    t.get_elevation_list()
    t.set_terrain_legend()
    # t.a_star((100, 230), (200, 230))
    # print(t.neighbors((100, 230)))
    # print(t.calculate_distance((100, 230), (200, 230)))
    # print(t.get_terrain_speed('#F89412'))

    # t.a_star((230, 327), (276, 279))

    # t.a_star((100, 230), (200, 230))
    #
    t.read_file()
    t.output_path()

    # for i in t.path:
    #     print(t.elevation_list[i[0]][i[1]])


if __name__ == '__main__':
    main()
