"""
Given a list of blocks, and each block contains some building, whose
value is either true or false. "true" indicates that the given block
has the given building.

Eg. Given block:
{
    "gym": true,
    "school": false
}
This block contains a gym, but not a school.

You are also given a list of requirements, containing all the buildings
in each block object.

You would like to buy an appartment in a block that is the most
convenient, i.e. it has the closest maximum distance from all the given
requirements. Find the best suiting block for your needs.
"""
import sys


def find_best_block(blocks: list[dict[str, bool]], reqs: list[str]) -> int:
    """Finds the best suiting block for your needs"""
    building_distances = [[sys.maxsize for _ in reqs] for _ in blocks]
    max_distances = [0 for _ in blocks]

    for j, building in enumerate(reqs):
        if blocks[0][building]:
            building_distances[0][j] = 0

    for i, block in enumerate(blocks[1:], start=1):
        for j, building in enumerate(reqs):
            if block[building]:
                building_distances[i][j] = 0
            else:
                new_building_distance = building_distances[i-1][j] + 1
                if new_building_distance < building_distances[i][j]:
                    building_distances[i][j] = new_building_distance

    for i, block in reversed(list(enumerate(blocks[:-1]))):
        for j, building in enumerate(reqs):
            if block[building]:
                building_distances[i][j] = 0
            else:
                new_building_distance = building_distances[i+1][j] + 1
                if new_building_distance < building_distances[i][j]:
                    building_distances[i][j] = new_building_distance

    for i, distances in enumerate(building_distances):
        max_distances[i] = max(distances)

    best_fit_block = 0
    smallest_max_distance = sys.maxsize
    for index, max_distance in enumerate(max_distances):
        if max_distance < smallest_max_distance:
            smallest_max_distance = max_distance
            best_fit_block = index

    return best_fit_block


def main() -> None:
    """Main function"""
    blocks = [
        {
            'gym': False,
            'school': True,
            'store': False,
        },
        {
            'gym': True,
            'school': False,
            'store': False,
        },
        {
            'gym': True,
            'school': True,
            'store': False,
        },
        {
            'gym': False,
            'school': True,
            'store': False,
        },
        {
            'gym': False,
            'school': True,
            'store': True,
        },
    ]
    reqs = ['gym', 'school', 'store']

    print(find_best_block(blocks, reqs))


if __name__ == '__main__':
    main()
