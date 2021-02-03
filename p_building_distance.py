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
# NOTE: naive solution. Use dynamic programming and 2 iterations (one
# from top and one from bottom) to get O(n) solution
from typing import Optional


def find_building_distance(
        blocks: list[dict[str, bool]],
        building: str,
        offset: int) -> int:
    """Returns the distance of nearest building from given index"""
    shortest_distance: Optional[int] = None

    for index, block in enumerate(blocks):
        if block[building]:
            distance = abs(offset - index)
            if shortest_distance is None or distance < shortest_distance:
                shortest_distance = distance

    assert shortest_distance is not None
    return shortest_distance


def find_best_block(blocks: list[dict[str, bool]]) -> int:
    """Finds the best suiting block for your needs"""
    min_total_distance: Optional[int] = None
    best_index = 0
    for index, block in enumerate(blocks):
        max_distance = 0
        for building in block:
            building_distance = find_building_distance(blocks, building, index)
            if building_distance > max_distance:
                max_distance = building_distance

        if min_total_distance is None or max_distance < min_total_distance:
            min_total_distance = max_distance
            best_index = index

    assert min_total_distance is not None
    return best_index


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
    # reqs = ['gym', 'school', 'store']

    print(find_best_block(blocks))


if __name__ == '__main__':
    main()
