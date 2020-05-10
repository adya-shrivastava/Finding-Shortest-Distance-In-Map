import math
import heapq
from _collections import deque
from PIL import Image

X_VALUE = 10.29
Y_VALUE = 7.55


def distance_cal(x1, x2, y1, y2):
    return math.sqrt(pow((x2 - x1) * X_VALUE, 2) + pow((y2 - y1) * Y_VALUE, 2))


def rgb_to_hex(rgb):
    return '#' + ('%02X%02X%02X' % rgb)

def get_terrain_speed(season, terrain_type):
    # terrain = {}
    if season == "summer":
        terrain = {'#F89412': ("Open land", 0),
                        '#FFC000': ("Rough meadow", 0),
                        '#FFFFFF': ("Easy movement forest", 0),
                        '#02D03C': ("Slow run forest", 0),
                        '#028828': ("Walk forest", 0),
                        '#054918': ("Impassible vegetation", 0),
                        '#0000FF': ("Lake/Swamp/Marsh", 0),
                        '#473303': ("Paved road", 0),
                        '#000000': ("Footpath", 0),
                        '#CD0065': ("Out of bounds", 0)}
    elif season =="winter":
        pass
    return terrain[terrain_type][1]

def neighbors(current):
    # print("\tin neighbors", current)
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
    # print("\tneighbor list", neighbor_list)
    return neighbor_list

def bfs():
    im = Image.open("terrain.png", 'r')
    # im.show()
    pix_val = im.load()
    pixel_values = [[None for j in range(500)] for i in range(395)]

    for i in range(395):
        for j in range(500):
            pixel_values[i][j] = rgb_to_hex(pix_val[i, j][:-1])

    visited_set = set()

    for i in range(len(pixel_values)):
        for j in range(len(pixel_values[0])):
            # if pixel_values[i][j] == "#0000FF":
            #     print(i, j)
            if pixel_values[i][j] == "#0000FF" and (i, j) not in visited_set:
                performBFS(pixel_values, i, j, visited_set)
                # print(visited_set)


def performBFS(pix_val, i, j, visited_set):
    src = (i, j)
    queue = deque()
    # queue.append((cost, src))
    # visited = {src: [0, None, 0]}
    # visited_set = set()
    # heapq.heappush(queue, src)
    queue.append(src)

    edges_set = set()

    while len(queue) > 0:
        # current = heapq.heappop(queue)
        current = queue.popleft()
        # print(current, "current")
        visited_set.add(current)

        for neighbor in neighbors(current):
            if neighbor not in visited_set:
                if pix_val[neighbor[0]][neighbor[1]] == "#0000FF":
                    # heapq.heappush(queue, neighbor)
                    queue.append(neighbor)
                else:
                    edges_set.add(neighbor)
    print(visited_set)
    return visited_set


def main():

    # bfs()
    # im = Image.open("terrain.png", 'r')
    # # im.show()
    # pix_val = list(im.getdata())
    # print(len(pix_val))
    # curr_list = [[None for j in range(500)] for i in range(395)]
    # for i in range(395):
    #     templist = pix_val[:500]
    #     for j in range(len(templist)):
    #         templist[j] = rgb_to_hex(templist[j][:-1])
    #     curr_list[i] = templist
    #
    # print(len(curr_list), len(curr_list[0]))
    #
    # # for x in pix_val:
    #     # print(x, rgb_to_hex(x[:-1]))
    #
    # file = open('mpp.txt', 'r')
    # elevation_list = []
    # count = 0
    # for i in file:
    #     x = str(i).split("   ")[1:]
    #     elevation_list.append(x[:-5])
    #     # print(len(x), x)
    #     count += 1
    # elevation_list = [[elevation_list[j][i] for j in range(len(elevation_list))] for i in range(len(elevation_list[0]))]
    #
    # # print(elevation_list)
    # print(len(elevation_list), len(elevation_list[0]))
    #
    # # print(count)
    # print(curr_list[100][230], curr_list[200][230])
    # pix_val = im.load()
    #
    # print("sfdhdskj", pix_val[4, 4])
    # print(pix_val[100, 230])
    # print(pix_val[334, 328])
    #
    # pix_val[100, 230] = (255, 0, 0, 255)
    # pix_val[230, 100] = (255, 0, 0, 255)
    #
    #
    #
    # # pix_val[200, 230] = (255, 0, 0, 255)
    #
    # print(distance_cal(100, 100, 130, 230))


    # im.show()

    print(rgb_to_hex((144, 78, 6)))



if __name__ == '__main__':
    main()