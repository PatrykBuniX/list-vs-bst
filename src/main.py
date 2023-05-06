import list as listTools
import tree as treeTools
import avl as avlTools
from data import generate_random_array
from time import perf_counter
import matplotlib.pyplot as plotter
from datetime import datetime
from tabulate import tabulate
import os
import numpy as np

REPEAT_COUNT = 10
SIZES_TO_MEASURE = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
                    10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000]


exampleArr = [10, 7, 18, 2, 9, 13, 4, 11, 15, 5, 17]
exampleBst = treeTools.construct_bst_tree(exampleArr)
print("Preorder traversal of the constructed BST")
treeTools.postorder(exampleBst)
exampleHeight = treeTools.get_height(exampleBst)
print(f"\nHeight of the constructed BST: {exampleHeight}")
exampleLevel = treeTools.get_level(exampleBst, 9)
print(f"Level of 9: {exampleLevel}")


def prepare_data(sizesToMeasure=SIZES_TO_MEASURE, repeatCount=REPEAT_COUNT):
    data = {}
    for size in sizesToMeasure:
        data[size] = {}
        for i in range(repeatCount):
            randomIntArr = generate_random_array(0, size, size)
            data[size][i] = randomIntArr

    return data


def do_measure(data, create_structure, find_node, remove_node, removeOrder=None, sizesToMeasure=SIZES_TO_MEASURE, repeatCount=REPEAT_COUNT):
    creationTimeData = []
    searchTimeData = []
    deleteTimeData = []
    sizeData = []
    for size in sizesToMeasure:
        sizeData.append(size)
        creationScores = []
        searchScores = []
        deleteScores = []
        for i in range(repeatCount):
            dataArr = data[size][i]
            # measure creation time
            cstart = perf_counter()
            head = create_structure(dataArr)
            cstop = perf_counter()
            creationTime = cstop - cstart
            creationScores.append(creationTime)
            print(
                f"\tcreation time of {size} size: {round(creationTime, 8)}s")

            # measure search time
            sstart = perf_counter()
            for item in dataArr:
                find_node(head, item)
            sstop = perf_counter()
            searchTime = sstop - sstart
            searchScores.append(searchTime)
            print(
                f"\tsearch time of {len(dataArr)} size: {round(searchTime, 8)}s")

            # measure delete time
            sortedData = reversed(
                dataArr) if removeOrder == "reversed" else sorted(dataArr)
            dstart = perf_counter()
            for item in sortedData:
                remove_node(head, item)
            dstop = perf_counter()
            deleteTime = dstop - dstart
            deleteScores.append(deleteTime)
            print(f"\tdeletion time of {size} size: {round(deleteTime, 8)}s")

        creationTimeData.append(sum(creationScores) / len(creationScores))
        searchTimeData.append(sum(searchScores) / len(searchScores))
        deleteTimeData.append(sum(deleteScores) / len(deleteScores))

    return sizeData, creationTimeData, searchTimeData, deleteTimeData


def create_chart(dataArr, title, xlabel, ylabel, yscale="linear", base=None):
    for item in dataArr:
        plotter.plot(item["xdata"], item["ydata"],
                     color=item["color"], label=item["label"])

    plotter.title(title)
    plotter.xlabel(xlabel)
    plotter.ylabel(ylabel)
    if base:
        plotter.yscale(yscale, base=base)
    else:
        plotter.yscale(yscale)
    plotter.grid()
    plotter.legend()
    now_time = datetime.now()

    dirname = os.path.dirname(__file__)
    filename = os.path.join(
        dirname, f"../report/bst-list/{title}_{yscale}_chart_{now_time}.png")

    try:
        plotter.savefig(filename)
    except FileExistsError:
        pass
    plotter.close(None)


def create_table(sizes, listTimes, treeTimes, title):
    now_time = datetime.now()

    dirname = os.path.dirname(__file__)
    filename = os.path.join(
        dirname, f"../report/bst-list/{title}_table_{now_time}_.txt")

    with open(filename, 'w') as f:
        table = [["n", "list", "bst"]]
        for i in range(len(sizes)):
            table.append([round(sizes[i], 8), round(
                listTimes[i], 8), round(treeTimes[i], 8)])
        f.write(tabulate(table, headers="firstrow"))
        f.close()


def measure_list_vs_bst():
    data = prepare_data(SIZES_TO_MEASURE, REPEAT_COUNT)
    print('measure list...')

    listSizes, listCreationTimes, listSearchTimes, listDeleteTimes = do_measure(data,
                                                                                listTools.construct_node_list, listTools.find_node, listTools.remove_node)
    print('measure tree...')
    treeSizes, treeCreationTimes, treeSearchTimes, treeDeleteTimes = do_measure(data,
                                                                                treeTools.construct_bst_tree, treeTools.find_node, treeTools.remove_node, "reversed")

    create_table(listSizes, listCreationTimes,
                 treeCreationTimes, "Tworzenie struktury")
    create_chart([
        {"xdata": listSizes, "ydata": listCreationTimes,
            "color": "red", "label": "lista"},
        {"xdata": treeSizes, "ydata": treeCreationTimes,
            "color": "green", "label": "drzewo"}
    ],
        "Tworzenie struktury",
        "liczba elementów",
        "czas [s]",
    )
    create_chart([
        {"xdata": listSizes, "ydata": listCreationTimes,
            "color": "red", "label": "lista"},
        {"xdata": treeSizes, "ydata": treeCreationTimes,
            "color": "green", "label": "drzewo"}
    ],
        "Tworzenie struktury",
        "liczba elementów",
        "czas [s]",
        "log"
    )

    create_table(listSizes, listSearchTimes,
                 treeSearchTimes, "Wyszukiwanie elementów")
    create_chart([
        {"xdata": listSizes, "ydata": listSearchTimes,
            "color": "red", "label": "lista"},
        {"xdata": treeSizes, "ydata": treeSearchTimes,
            "color": "green", "label": "drzewo"}
    ],
        "Wyszukiwanie elementów",
        "liczba elementów",
        "czas [s]",
    )
    create_chart([
        {"xdata": listSizes, "ydata": listSearchTimes,
            "color": "red", "label": "lista"},
        {"xdata": treeSizes, "ydata": treeSearchTimes,
            "color": "green", "label": "drzewo"}
    ],
        "Wyszukiwanie elementów",
        "liczba elementów",
        "czas [s]",
        "log"
    )

    create_table(listSizes, listDeleteTimes,
                 treeDeleteTimes, "Usuwanie elementów")

    create_chart([
        {"xdata": listSizes, "ydata": listDeleteTimes,
            "color": "red", "label": "lista"},
        {"xdata": treeSizes, "ydata": treeDeleteTimes,
            "color": "green", "label": "drzewo"}
    ],
        "Usuwanie elementów",
        "liczba elementów",
        "czas [s]",
    )
    create_chart([
        {"xdata": listSizes, "ydata": listDeleteTimes,
            "color": "red", "label": "lista"},
        {"xdata": treeSizes, "ydata": treeDeleteTimes,
            "color": "green", "label": "drzewo"}
    ],
        "Usuwanie elementów",
        "liczba elementów",
        "czas [s]",
        "log"
    )


def measure_bst_vs_avl_heights():
    data = prepare_data(SIZES_TO_MEASURE, REPEAT_COUNT)
    bstHeights = []
    avlHeights = []

    for size in SIZES_TO_MEASURE:
        bstScores = []
        avlScores = []
        for i in range(REPEAT_COUNT):
            dataArr = data[size][i]
            bstHead = treeTools.construct_bst_tree(dataArr)
            avlHead = avlTools.construct_avl_tree(dataArr)

            bstHeight = treeTools.get_height(bstHead)
            avlHeight = avlTools.get_height(avlHead)

            bstScores.append(bstHeight)
            avlScores.append(avlHeight)

        bstHeightAvg = sum(bstScores) // len(bstScores)
        bstHeights.append(bstHeightAvg)

        avlHeightAvg = sum(avlScores) // len(avlScores)
        avlHeights.append(avlHeightAvg)

        print(f"size: {size}, bst: {bstHeightAvg}, avl: {avlHeightAvg}")

    barWidth = 0.25
    plotter.subplots(figsize=(16, 8))

    br1 = np.arange(len(avlHeights))
    br2 = [x + barWidth for x in br1]

    plotter.bar(br1, avlHeights, color='lightgreen',
                width=barWidth, label='AVL')
    plotter.bar(br2, bstHeights, color='green',
                width=barWidth, label='BST')

    plotter.title("Porównanie wysokości BST i AVL")
    plotter.xlabel('Liczba elementów')
    plotter.ylabel('Wysokość drzewa')
    plotter.xticks([r + barWidth for r in range(len(avlHeights))],
                   map(lambda x: f"{x//1000}k", SIZES_TO_MEASURE))

    plotter.legend()

    title = "avl_bst_heights"

    now_time = datetime.now()
    dirname = os.path.dirname(__file__)
    filename = os.path.join(
        dirname, f"../report/bst-avl/{title}_chart_{now_time}.png")

    try:
        plotter.savefig(filename)
    except FileExistsError:
        pass
    plotter.close(None)

    dirname = os.path.dirname(__file__)
    filename = os.path.join(
        dirname, f"../report/bst-avl/{title}_table_{now_time}_.txt")

    with open(filename, 'w') as f:
        table = [["n", "bst height", "avl height"]]
        for i in range(len(SIZES_TO_MEASURE)):
            table.append([SIZES_TO_MEASURE[i], bstHeights[i], avlHeights[i]])
        f.write(tabulate(table, headers="firstrow"))
        f.close()


# measure_list_vs_bst()
# measure_bst_vs_avl_heights()
