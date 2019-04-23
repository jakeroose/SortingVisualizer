from random import randint


NUM_COUNT = 50
SHUFFLE_AMOUNT = 50

def main():
    # initialize array
    lines = []
    for i in range(1, NUM_COUNT+1):
        lines.append(i)

    # shuffle array
    shuffle(lines)

    mSort = MergeSort(lines)
    mSort.perform(0, len(lines)-1)

# Shuffles our array
def shuffle(lines):
    for i in range(1, SHUFFLE_AMOUNT):
        i1 = randint(0, NUM_COUNT-1)
        i2 = randint(0, NUM_COUNT-1)

        # swap
        lines[i1], lines[i2] = lines[i2], lines[i1]

def swap(lines, i1, i2):
    lines[i1], lines[i2] = lines[i2], lines[i1]

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

        middle, index = int((start + stop)/2), start
        left, right = self.lines[start:middle+1], self.lines[middle+1:stop+1]

        print("\n==== Merge Result====")
        print("Merge " + str(start) + "->" + str(middle) + "->" + str(stop))

        while len(left) > 0 and len(right) > 0:
            if left[0] <= right[0]:
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

        for r in result:
            self.lines[index] = r
            print(str(r) + "\t" + str(self.lines[index]))
            index += 1
        print("=====================")

        return result


main()
