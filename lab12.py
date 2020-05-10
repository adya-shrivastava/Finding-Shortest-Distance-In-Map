import math
import heapq
import sys
from collections import deque

from PIL import Image

X_VALUE = 10.29
Y_VALUE = 7.55
UP = 0.5
DOWN = 1.25


class Terrain:
    __slots__ = "terrain_image", "elevation_file", "path_file", "output_image_filename", "season", "terrain_legend", \
                "pixel_values", "elevation_list", "path", "total_distance", "im", "pix_val"

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
        self.im = Image.open(self.terrain_image, "r")

    def set_terrain_legend(self):
        if self.season == "summer":
            self.terrain_legend = {'#F89412': ("Open land", 2.8),
                                   '#FFC000': ("Rough meadow", 0.8),
                                   '#FFFFFF': ("Easy movement forest", 2.3),
                                   '#02D03C': ("Slow run forest", 0.85),
                                   '#028828': ("Walk forest", 0.7),
                                   '#054918': ("Impassible vegetation", 0.1),
                                   '#0000FF': ("Lake/Swamp/Marsh", 0.000001),
                                   '#473303': ("Paved road", 2.8),
                                   '#000000': ("Footpath", 2.5),
                                   '#CD0065': ("Out of bounds", 0.000001)}
        elif self.season == "fall":
            self.terrain_legend = {'#F89412': ("Open land", 2.8),
                                   '#FFC000': ("Rough meadow", 0.8),
                                   '#FFFFFF': ("Easy movement forest", 1.5),
                                   '#02D03C': ("Slow run forest", 0.85),
                                   '#028828': ("Walk forest", 0.7),
                                   '#054918': ("Impassible vegetation", 0.1),
                                   '#0000FF': ("Lake/Swamp/Marsh", 0.000001),
                                   '#473303': ("Paved road", 2.8),
                                   '#000000': ("Footpath", 2.5),
                                   '#CD0065': ("Out of bounds", 0.000001)}
        elif self.season == "winter":
            self.color_winter("winter")
            self.terrain_legend = {'#F89412': ("Open land", 2.8),
                                   '#FFC000': ("Rough meadow", 0.8),
                                   '#FFFFFF': ("Easy movement forest", 2.3),
                                   '#02D03C': ("Slow run forest", 0.85),
                                   '#028828': ("Walk forest", 0.7),
                                   '#054918': ("Impassible vegetation", 0.1),
                                   '#0000FF': ("Lake/Swamp/Marsh", 0.000001),
                                   '#473303': ("Paved road", 2.8),
                                   '#000000': ("Footpath", 2.5),
                                   '#CD0065': ("Out of bounds", 0.000001),
                                   '#33FFFF': ("Frozen Water", 2.5)
                                   }

        elif self.season == "spring":
            self.color_winter("spring")
            self.terrain_legend = {'#F89412': ("Open land", 2.8),
                                   '#FFC000': ("Rough meadow", 0.8),
                                   '#FFFFFF': ("Easy movement forest", 2.3),
                                   '#02D03C': ("Slow run forest", 0.85),
                                   '#028828': ("Walk forest", 0.7),
                                   '#054918': ("Impassible vegetation", 0.1),
                                   '#0000FF': ("Lake/Swamp/Marsh", 0.000001),
                                   '#473303': ("Paved road", 2.8),
                                   '#000000': ("Footpath", 2.5),
                                   '#CD0065': ("Out of bounds", 0.000001),
                                   '#33FFFF': ("Mud", 0.7)
                                   }

    def get_terrain_speed(self, terrain):
        return self.terrain_legend[terrain][1]

    def get_pixel_values(self):
        # im = Image.open(self.terrain_image, "r")
        # pix_val = im.load()
        self.pix_val = self.im.load()

        self.pixel_values = [[None for j in range(500)] for i in range(395)]

        for i in range(395):
            for j in range(500):
                self.pixel_values[i][j] = rgb_to_hex(self.pix_val[i, j][:-1])

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

        # print(len(self.elevation_list), len(self.elevation_list[0]))

    def calculate_distance(self, src, dest):
        x1, y1 = src
        x2, y2 = dest
        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)
        return math.sqrt(pow((x2 - x1) * X_VALUE, 2) + pow((y2 - y1) * Y_VALUE, 2) +
                         pow(float(self.elevation_list[x1][y1]) - float(self.elevation_list[x2][y2]), 2))

    def calculate_heuristic(self, src, dest):
        speed = self.get_terrain_speed('#F89412')
        return self.calculate_distance(src, dest) / speed

    def calculate_speed(self, src, dest):
        speed = self.get_terrain_speed(self.pixel_values[dest[0]][dest[1]])
        elevation = float(self.elevation_list[dest[0]][dest[1]]) - float(self.elevation_list[src[0]][src[1]]) * -1
        # tan_val = (float(self.elevation_list[dest[0]][dest[1]]) - float(self.elevation_list[src[0]][src[1]])) / (self.calculate_distance(src, dest))

        if float(self.elevation_list[dest[0]][dest[1]]) - float(self.elevation_list[src[0]][src[1]]) < 0:
            speed = speed * DOWN * elevation
        elif float(self.elevation_list[dest[0]][dest[1]]) - float(self.elevation_list[src[0]][src[1]]) > 0:
            speed = speed * UP * elevation

        return speed

    def reachable(self, current):
        return self.pixel_values[current[0]][current[1]] != '#CD0065' and self.pixel_values[current[0]][current[1]] != '#0000FF'

    def neighbors(self, current):
        i, j = current
        neighbor_list = []
        if i - 1 >= 0 and j - 1 >= 0:
            neighbor_list.append((i - 1, j - 1))
        if i - 1 >= 0 and j >= 0:
            neighbor_list.append((i - 1, j))
        if i - 1 >= 0 and j + 1 < 500:
            neighbor_list.append((i - 1, j + 1))
        if i >= 0 and j - 1 >= 0:
            neighbor_list.append((i, j - 1))
        if i + 1 < 395 and j - 1 >= 0:
            neighbor_list.append((i + 1, j - 1))
        if i >= 0 and j + 1 < 500:
            neighbor_list.append((i, j + 1))
        if i + 1 < 395 and j + 1 < 500:
            neighbor_list.append((i + 1, j + 1))
        if i + 1 < 395 and j < 500:
            neighbor_list.append((i + 1, j))
        return neighbor_list

    def read_file(self):
        file = open(self.path_file)
        file = file.readlines()
        for i in range(len(file) -1):
            src = tuple(int(s) for s in file[i].strip().split(" "))
            dest = tuple(int(s) for s in file[i+1].strip().split(" "))
            self.a_star(src, dest)

    def color_winter(self, season):
        edges_set = set()
        for i in range(395):
            for j in range(500):
                if self.pixel_values[i][j] == "#0000FF":
                    for neighbor in self.neighbors((i, j)):
                        if self.pixel_values[neighbor[0]][neighbor[1]] != "#0000FF" and neighbor not in edges_set:
                            edges_set.add((neighbor[0], neighbor[1]))

        # print(edges_set)
        if season == "winter":
            self.performBFS(edges_set)
        elif season == "spring":
            self.performBFS_spring(edges_set)

    def performBFS(self, edges_set):

        queue = deque(list(edges_set))

        # queue.append(i for i in list(edges_set))
        queue.append("null")
        # print(queue)
        level = 0
        while len(queue) > 0:
            current = queue.popleft()
            # print(current)

            if current == "null":
                level += 1
                if level == 6:
                    break
                queue.append("null")
                continue

            for neighbor in self.neighbors(current):
                if self.pixel_values[neighbor[0]][neighbor[1]] == "#0000FF" and neighbor not in edges_set:
                    edges_set.add(neighbor)
                    queue.append(neighbor)
        self.pix_val = self.im.load()

        for edge in edges_set:
            (x, y) = edge
            if self.pix_val[x, y] != (0,0,0,255):
                self.pix_val[x, y] = (51, 255, 255)

    def performBFS_spring(self, edges_set):

        queue = deque(list(edges_set))

        # queue.append(i for i in list(edges_set))
        queue.append("null")
        # print(queue)
        level = 0
        while len(queue) > 0:
            current = queue.popleft()
            # print(current)

            if current == "null":
                level += 1
                if level == 14:
                    break
                queue.append("null")
                continue

            for neighbor in self.neighbors(current):
                if self.pixel_values[neighbor[0]][neighbor[1]] != "#0000FF" and self.pixel_values[neighbor[0]][neighbor[1]] != "#CD0065" \
                        and neighbor not in edges_set and (float(self.elevation_list[neighbor[0]][neighbor[1]]) - float(self.elevation_list[current[0]][current[1]])) <= 1:
                    edges_set.add(neighbor)
                    queue.append(neighbor)

        self.pix_val = self.im.load()

        for edge in edges_set:
            (x, y) = edge
            self.pix_val[x, y] = (144, 78, 6)

    def a_star(self, src, dest):
        queue = []
        cost = 0 + self.calculate_heuristic(src, dest)
        visited = {src: [0, None, 0]}
        visited_set = set()
        heapq.heappush(queue, (cost, src))
        visited_set.add(src)

        while len(queue) > 0:
            current = heapq.heappop(queue)
            visited_set.add(current[1])
            # print(len(queue))

            if current[1] == dest:
                break

            for neighbor in self.neighbors(current[1]):
                if self.reachable(neighbor):
                    distance = self.calculate_distance(current[1], neighbor)
                    speed = self.calculate_speed(current[1], neighbor)
                    # print(current[1], neighbor, distance, speed)
                    cost = (distance / speed) + self.calculate_heuristic(neighbor, dest) + current[0]
                    if neighbor not in visited_set:
                        if neighbor in visited:
                            if cost < visited[neighbor][0]:
                                queue.remove((visited[neighbor][0], neighbor))
                                heapq.heappush(queue, (cost, neighbor))
                                visited[neighbor] = [cost, current[1], distance]

                        else:
                            heapq.heappush(queue, (cost, neighbor))
                            visited[neighbor] = [cost, current[1], distance]
            # print(queue)
        if dest in visited_set:
            current = dest
            path = []
            while current != src:
                path.insert(0, current)
                # print(visited[current][2])
                self.total_distance += visited[current][2]
                current = visited[current][1]

            path.insert(0, src)

            self.path.append(path)

    def output_path(self):
        # im = Image.open(self.terrain_image, "r")
        # file = im.load()

        self.path = [i for j in self.path for i in j]
        print("Path taken", self.path)
        print("Total distance travelled", self.total_distance)
        for i in self.path:
            # file[i] = (255, 0, 0, 255)
            self.pix_val[i] = (139, 0, 139, 255)

        self.im = self.im.save(self.output_image_filename)


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
    t.read_file()
    t.output_path()


if __name__ == '__main__':
    main()
