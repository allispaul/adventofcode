def parse_input(filename):
    # Return (1) code string (2) an Image object containing the image
    lines = open(filename, 'r').read().split('\n')
    list_of_strings = []
    for line in lines[1:]:
        if line == '':
            continue
        list_of_strings.append(line)
    code = ''.join([char for char in lines[0] if char in {'.', '#'}])
    assert len(code) == 512
    return code, Image(list_of_strings)

class Image():

    def __init__(self, list_of_strings, boundary=False):
        # boundary is the status of the pixels on the boundary
        self.ymax = len(list_of_strings)
        self.xmax = len(list_of_strings[0])
        self.boundary = boundary
        self.array = []
        for s in list_of_strings:
            assert len(s) == self.xmax
            row = []
            for x in s:
                if x == ".":
                    row.append(False)
                elif x == "#":
                    row.append(True)
                else:
                    raise ValueError(f"Forbidden character '{x}' in image.")
            self.array.append(row)

    def __repr__(self):
        repr = ""
        for row in self.array:
            for x in row:
                if x:
                    repr += "#"
                else:
                    repr += "."
            repr += "\n"
        return repr[:-1]

    def get(self, x, y):
        if x >= self.xmax or x < 0 or y >= self.ymax or y < 0:
            return self.boundary
        return self.array[y][x]

    def expand(self):
        # Expand by 1 pixel in each direction
        self.xmax += 2
        self.ymax += 2
        self.array = [[self.boundary] * self.xmax] + \
            [([self.boundary] + row + [self.boundary]) for row in self.array] + \
            [[self.boundary] * self.xmax]

    def shrink(self):
        # Shrink by 1 pixel in each direction
        self.array = [row[1:self.xmax-1] for row in self.array[1:self.ymax-1]]
        self.xmax -= 2
        self.ymax -= 2

    def surroundings_to_binary(self, x, y):
        return (2**8*self.get(x-1,y-1) + 2**7*self.get(x,y-1) + 2**6*self.get(x+1,y-1)
                + 2**5*self.get(x-1,y) + 2**4*self.get(x,y) + 2**3*self.get(x+1,y)
                + 2**2*self.get(x-1,y+1) + 2*self.get(x,y+1) + self.get(x+1,y+1))

    def enhance(self, code):
        # Apply the code to enhance self
        self.expand()
        list_of_strings = []
        for y in range(self.ymax):
            row = ""
            for x in range(self.xmax):
                row += code[self.surroundings_to_binary(x, y)]
            list_of_strings.append(row)
        # Check boundary condition
        if self.boundary:
            boundary = (code[511] == "#")
        else:
            boundary = (code[0] == "#")
        self.shrink()
        return Image(list_of_strings, boundary)

    def count_lit_pixels(self):
        # Return the number of lit pixels.
        if self.boundary == True:
            raise OverflowError("Infinitely many lit pixels.")
        pixels = [p for row in self.array for p in row]
        return pixels.count(True)

    def enhance_n_times(self, code, n, verbose=False):
        img = self
        for i in range(n):
            if verbose:
                print(f"Enhancing {i+1} times...")
            img = img.enhance(code)
        return img


def test():
    code, img = parse_input("test20.txt")
    # print(img)
    # print('')
    img.expand()
    # print(img)
    # print('')
    img.shrink()
    # print(img)
    # print('')

    assert img.surroundings_to_binary(2,2) == 34

    img = img.enhance(code)
    # print(img)
    # print('')
    img = img.enhance(code)
    # print(img)
    # print('')
    assert img.count_lit_pixels() == 35
    img = img.enhance_n_times(code, 48, verbose=True)
    assert img.count_lit_pixels() == 3351

def main():
    code, img = parse_input("input20.txt")
    img = img.enhance(code)
    img = img.enhance(code)
    print(img.count_lit_pixels())
    img = img.enhance_n_times(code, 48, verbose=True)
    print(img.count_lit_pixels())
