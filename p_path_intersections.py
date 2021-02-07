"""
You are given two paths to choose from, and each path has a bunch of
sorted numbers (points) on it.

The paths are said to "intersect" at any two given indices if those
indices have the same number. You are allowed to follow any of the two
paths after an intersection.

You start at any one path, and you have to reach the end of any of the
two paths, while collecting the maximum amount of points. Find the
maximum number of points you can collect.
"""


def max_points(path1: list[int], path2: list[int]) -> int:
    """Returns the maximum points you can collect on the paths"""
    intersections = set(path1) & set(path2)

    index1, index2 = 0, 0
    end1, end2 = len(path1), len(path2)
    points = 0

    point1 = path1[index1]
    point2 = path2[index2]
    while index1 < end1 or index2 < end2:
        path_sum1 = 0
        path_sum2 = 0

        while index1 < end1:
            point1 = path1[index1]
            path_sum1 += point1
            if point1 in intersections:
                break

            index1 += 1

        while index2 < end2:
            point2 = path2[index2]
            path_sum2 += point2
            if point2 in intersections:
                break

            index2 += 1

        max_path_sum = path_sum1 if path_sum1 > path_sum2 else path_sum2
        points += max_path_sum

        index1 += 1
        index2 += 1

    return points


def main() -> None:
    """Main function"""
    path1 = [1, 3, 5, 8, 10, 12, 14]
    path2 = [2, 5, 6, 7, 8, 11, 13, 14, 16, 17]

    print(max_points(path1, path2))


if __name__ == '__main__':
    main()
