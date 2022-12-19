from dataclasses import dataclass


class Directory():
    def __init__(self, name, parent=None):
        self.name = name
        self.children = []
        self.parent = parent

    def __repr__(self):
        repr = f"Directory {self.name} (size {self.get_size()})"
        return repr

    def add_child(self, child):
        self.children.append(child)

    def get_size(self):
        return sum(child.get_size() for child in self.children)

    def subdirectories(self):
        """Return a list of all subdirectories (evaluated recursively),
        including self.
        """
        dirs = [self]
        for child in self.children:
            if type(child) is Directory:
                dirs += child.subdirectories()
        return dirs

    def little_kids(self):
        """Recursively get all subdirectories of self of size at most 100000.
        """
        return [d for d in self.subdirectories() if d.get_size() <= 100000]


@dataclass
class File():
    name: str
    size: int
    parent: Directory

    def get_size(self):
        return self.size


class FileTree():
    def __init__(self):
        self.root = Directory("/")
        # self.pos should always be a directory
        self.pos = self.root

    def move_up(self):
        self.pos = self.pos.parent

    def move_to_child(self, name):
        for child in self.pos.children:
            if child.name == name:
                self.pos = child
                break
        else:
            raise KeyError(f"{name} not in {self.pos}.")
        # I just learned about for-else and it looks so stupid but I keep
        # finding reasons to use it

    def move_to_root(self):
        self.pos = self.root

    def add_file(self, name, size):
        f = File(name, size, self.pos)
        self.pos.add_child(f)

    def add_dir(self, name):
        d = Directory(name, self.pos)
        self.pos.add_child(d)

    def parse_command(self, cmd):
        if cmd == "$ cd /":
            self.move_to_root()
        elif cmd == "$ cd ..":
            self.move_up()
        elif cmd.startswith("$ cd "):
            self.move_to_child(cmd[5:])
        elif cmd == "$ ls":
            # We can ignore these -- we know they'll be followed by a list of children
            pass
        elif cmd.startswith("dir "):
            # Child directory of current position
            self.add_dir(cmd.split()[1])
        else:
            # Child file of current position
            size, name = cmd.split()
            self.add_file(name, int(size))
            # Throws an error if the first word is not numeric

    def dirs(self):
        return self.root.subdirectories()

    def smallest_deletable_dir(self):
        total_space = 70000000
        needed_space = 30000000

        used_space = self.root.get_size()
        avail_space = total_space - used_space
        space_to_free = needed_space - avail_space
        return min((d for d in self.dirs() if d.get_size() >= space_to_free),
                   key=Directory.get_size)


def parse_terminal_output(filename):
    tree = FileTree()
    with open(filename, 'r') as lines:
        for line in lines:
            # remove trailing newline
            tree.parse_command(line[:-1])
    return tree




if __name__ == "__main__":
    # part a
    tree1 = parse_terminal_output("test7.txt")
    assert tree1.root.get_size() == 48381165
    print(tree1.root.little_kids())
    assert sum(kid.get_size() for kid in tree1.root.little_kids()) == 95437

    tree = parse_terminal_output("input7.txt")
    print(sum(kid.get_size() for kid in tree.root.little_kids()))

    # part b
    tree1 = parse_terminal_output("test7.txt")
    print(tree1.smallest_deletable_dir())

    tree = parse_terminal_output("input7.txt")
    print(tree.smallest_deletable_dir())
