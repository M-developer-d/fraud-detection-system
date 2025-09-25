print("Loading.............")
n = int(input("enter:"))
tuple_list = []
for i in range(n):
    t = tuple(map(int, input().split()))
    print(t)
    print(hash(t))

    # if __name__ == '__main__':
    # n = int(input())
    #
    # print(hash(t))