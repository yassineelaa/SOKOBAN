def print_grid(g): #debug
    for y in range(len(g)):
        for x in range(len(g[y])):
            print(g[y][x], end=" ")
        print("")

def get_y(y, dir, step):
    if dir == "l" or dir == "r":
        return y
    elif dir == "u":
        return y-step
    elif dir == "d":
        return y+step

def get_x(x, dir, step):
    if dir == "u" or dir == "d":
        return x
    elif dir == "l":
        return x-step
    elif dir == "r":
        return x+step
