from graphics import *
from random import randint

# https://mcsp.wartburg.edu//zelle/python/graphics/graphics/index.html
# Algorithms implemented from Wikipedia:
# https://en.wikipedia.org/wiki/Sorting_algorithm

# TODO:
# Fix HeapSort
# Display name of current algorithm, number of swaps, and step delay in window

WIN_WIDTH = 1000
WIN_HEIGHT = 750
NUM_COUNT = 100
LINE_WIDTH = WIN_WIDTH / NUM_COUNT
STEP_DELAY = 20.0 # delay between swaps
SORT_UPDATE_RATE = 1000/STEP_DELAY
SHUFFLE_AMOUNT = 200
LINE_COLOR = color_rgb(200,200,200)
LINE_HIGHLIGHT_COLOR = color_rgb(200,0,0)

def main():
    win = GraphWin("Sorting demo", WIN_WIDTH, WIN_HEIGHT, autoflush=False)
    win.setBackground(color_rgb(0,0,0))

    # initialize array
    lines = []
    for i in range(1, NUM_COUNT+1):
        ln = LineInfo(i*2, i)
        ln.draw(win)
        lines.append(ln)
        update()

    # shuffle array
    shuffle(lines)

    # Bubble Sort
    # bSort = BubbleSort(lines)
    # bSort.perform()
    # # sleep for a sec to look at it
    # shuffle(lines)

    # Quick Sort
    # qSort = QuicksortLomuto(lines)
    # qSort.perform(0, NUM_COUNT-1)

    # Merge Sort
    mSort = MergeSort(lines)
    mSort.perform(0, len(lines)-1)

    # Heap Sort
    # hSort = HeapSort(lines)
    # hSort.heapSort()

    win.getMouse()
    win.close()

# Shuffles our array
def shuffle(lines):
    for i in range(1, SHUFFLE_AMOUNT):
        i1 = randint(0, NUM_COUNT-1)
        i2 = randint(0, NUM_COUNT-1)

        swap(lines, i1, i2, False)

def swap(lines, i, j, throttle=True):
    # swap lines[i] and lines[j]
    tmp = lines[i]
    lines[i] = lines[j]
    lines[j] = tmp
    lines[i].update_position(i)
    lines[j].update_position(j)

    # highlight line to show it's being swapped
    setColor(lines[i], LINE_HIGHLIGHT_COLOR)
    setColor(lines[j], LINE_HIGHLIGHT_COLOR)

    if throttle:
        update(SORT_UPDATE_RATE)
    else:
        update()

    # set back to normal color for next time update() is called
    setColor(lines[i], LINE_COLOR)
    setColor(lines[j], LINE_COLOR)

def setColor(line, color):
    line.line.setFill(color)
    line.line.setOutline(color)

class BubbleSort:
    def __init__(self, lines):
        self.swapped = False
        self.index = 0
        self.lines = lines
        self.steps = 0

    def perform(self):
        n = len(self.lines)
        swapped = True
        while swapped is True:
            swapped = False
            for i in range(n-1):
                if self.lines[i].val > self.lines[i + 1].val:
                    self.index = i
                    self.swap()
                    swapped = True
                update(SORT_UPDATE_RATE)
            n = n - 1

    # Sorts by calling step() in a loop until it returns False
    def step(self):
        self.steps += 1
        # print("step")
        if self.index is 0:
            self.swapped = False
        if self.lines[self.index].val > self.lines[self.index+1].val:
            self.swap()
            self.swapped = True

        # returns false when sorting is done
        if self.swapped is False and self.index == (NUM_COUNT - 1):
            return False

        self.index = (self.index + 1) % (NUM_COUNT - 1)
        return True

    def swap(self):
        tmp = self.lines[self.index]
        self.lines[self.index] = self.lines[self.index + 1]
        self.lines[self.index + 1] = tmp
        self.lines[self.index].update_position(self.index)
        self.lines[self.index + 1].update_position(self.index + 1)

# Doesn't currenlty work, goes out of bounds
class QuicksortHoare:

    def __init__(self, lines):
        self.lines = lines

    def perform(self, low, high):
        if low < high:
            p = self.partition(low, high)
            self.perform(low, p)
            self.perform(p + 1, high)

    def partition(self, low, high):
        pivot = self.lines[(low+high) / 2].val
        i = low - 1
        j = high + 1
        while True:
            while self.lines[i].val < pivot:
                i += 1
            while self.lines[j].val > pivot:
                j -= 1
            if i >= j:
                return j

            # swap lines[i] and lines[j]
            tmp = self.lines[i]
            self.lines[i] = self.lines[j]
            self.lines[j] = tmp
            self.lines[i].update_position(i)
            self.lines[j].update_position(j)
            update(SORT_UPDATE_RATE)

# Uses Lomuto algorithm to pick pivot point for Quick Sort algorithm
class QuicksortLomuto:

    def __init__(self, lines):
        self.lines = lines

    def perform(self, low, high):
        if low < high:
            p = self.partition(low, high)
            self.perform(low, p - 1)  # sort 1st half of partition
            self.perform(p + 1, high) # sort 2nd half of partition

    def partition(self, low, high):
        pivot = self.lines[high].val
        i = low
        for j in range(low, high):
            if self.lines[j].val < pivot:
                swap(self.lines, i, j)
                update(SORT_UPDATE_RATE)
                i += 1

        swap(self.lines, i, high)
        update(SORT_UPDATE_RATE)

        return i

# Heap Sort WIP
class HeapSort:

    def __init__(self, lines):
        self.lines = lines

    # def heapsort(self, count):
    #     end = count - 1
    #     while end > 0:
    #         swap(lines, end, 0)
    #         end -= 1
    #         siftDown(0, end)
    #
    # def heapify(self, count):
    #     start = iParent(count - 1)
    #
    #     while start >= 0:
    #         siftDown(start, count-1)
    #         start = start-1

    # def iLeftCihld(self, start, end):
    #     root = start
    #
    #     while iLeftCihld(root) <= end:
    #         child = iLeftChild(root)

    # To heapify subtree rooted at index i.
    # n is size of heap
    def heapify(self, n, i):
        largest = i # Initialize largest as root
        l = 2 * i + 1     # left = 2*i + 1
        r = 2 * i + 2     # right = 2*i + 2

        # See if left child of root exists and is
        # greater than root
        if l < n and self.lines[i] < self.lines[l]:
            largest = l

        # See if right child of root exists and is
        # greater than root
        if r < n and self.lines[largest] < self.lines[r]:
            largest = r

        # Change root, if needed
        if largest != i:
            swap(self.lines, i, largest)

            # Heapify the root.
            self.heapify(n, largest)

    # The main function to sort an array of given size
    def heapSort(self):
        n = len(self.lines)

        # Build a maxheap.
        for i in range(n, -1, -1):
            self.heapify(n, i)

        # One by one extract elements
        for i in range(n-1, 0, -1):
            swap(self.lines, i, 0)
            self.heapify(i, 0)


# Merge Sort algorithm
class MergeSort:

    def __init__(self, lines):
        self.lines = lines

    def perform(self, start, stop):
        # Base case
        if stop == start:
            return

        middle = int((start + stop) / 2)

        self.perform(start, middle) # left
        self.perform(middle + 1, stop) # right

        return self.mergeCopy(start, stop)

    def mergeCopy(self, start, stop):
        result = []

        # index is used to store merge back into self.lines
        middle, index = int((start + stop)/2), start
        left, right = self.lines[start:middle+1], self.lines[middle+1:stop+1]

        # print("\n==== Merge Info ====")
        # print("Merge " + str(start) + "->" + str(middle) + "->" + str(stop))

        while len(left) > 0 and len(right) > 0:
            if left[0].val <= right[0].val:
                result.append(left[0])
                left = left[1:]
            else:
                result.append(right[0])
                right = right[1:]
        while len(left) > 0:
            result.append(left[0])
            left = left[1:]
        while len(right) > 0:
            result.append(right[0])
            right = right[1:]

        # Move numbers in self.lines to correct positions
        for r in result:
            swap(self.lines, r.order, index)
            index += 1
            update()

# Creates a visual representation of the numbers we're sorting
class LineInfo:

    def __init__(self, val, order):
        self.val = val # integer value of the line
        self.order = order # current order of the line
        self.line = None # Rectangle from graphics.py used to draw to window
        self.update_position(order) # initialize position

        self.line.setOutline(LINE_COLOR)
        self.line.setFill(LINE_COLOR)

    def __repr__(self):
        return "LineInfo(val={}, order={})".format(self.val, self.order)

    # updates it's position when it's value has been changed
    def update_position(self, order):
        self.order = order

        # pt1 = bottom left of line, pt2 = top right of line
        self.pt1 = Point((self.order - 1) * LINE_WIDTH, WIN_HEIGHT)
        self.pt2 = Point((self.order - 1) * LINE_WIDTH + LINE_WIDTH - 1, WIN_HEIGHT - self.val)

        if self.line is not None:
            # Line exists, so move it to new position
            self.line.move(self.pt1.x - self.line.p1.x + LINE_WIDTH, 0)
        else:
            # Line Rectangle needs to be created
            self.line = Rectangle(self.pt1, self.pt2)


    def draw(self, win):
        self.line.draw(win)

main()
