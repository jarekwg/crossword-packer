import re
from exceptions import WordPlacementConflict

from constants import ACROSS, DOWN


def score_placements(placements, display=False):
    dimensions = [
        min([x for x, y, dir in placements.values()]),
        min([y for x, y, dir in placements.values()]),
        max([placement[0] + len(word) for word, placement in placements.items() if placement[2] == ACROSS] + [x + 1 for x, y, dir in placements.values()]),
        max([placement[1] + len(word) for word, placement in placements.items() if placement[2] == DOWN] + [y + 1 for x, y, dir in placements.values()]),
    ]

    width = dimensions[2] - dimensions[0]
    height = dimensions[3] - dimensions[1]
    x_offset = dimensions[0]
    y_offset = dimensions[1]

    lines = []
    for _ in range(height):
        lines.append('.' * width)

    numintersections = 0

    for word, placement in placements.items():
        x = placement[0] - x_offset
        y = placement[1] - y_offset
        if placement[2] == ACROSS:
            # If letters before or after aren't empty, bail out.
            if (placement[0] - 1 >= dimensions[0] and lines[y][x - 1] != '.') or (placement[0] + len(word) < dimensions[2] and lines[y][x + len(word)] != '.'):
                raise WordPlacementConflict
            # If incoming letters don't match existing letters, bail out.
            if re.match(lines[y][x:x + len(word)], word) is None:
                raise WordPlacementConflict
            # Check neighbouring rows. Bail out if there's something in them for words that aren't intersecting.
            for row_offset in [-1, 1]:
                if dimensions[1] <= placement[1] + row_offset < dimensions[3]:
                    for i, c in enumerate(lines[y + row_offset][x:x + len(word)]):
                        if c != '.' and lines[y][x + i] == '.':
                            raise WordPlacementConflict
            # Increment numintersections for every matching existing letter (ie. intersection)
            numintersections += len(set(lines[y][x:x + len(word)].replace('.', '')))
            lines[y] = lines[y][:x] + word + lines[y][x + len(word):]
        else:
            # If letters before or after aren't empty, bail out.
            if (placement[1] - 1 >= dimensions[1] and lines[y - 1][x] != '.') or (placement[1] + len(word) < dimensions[3] and lines[y + len(word)][x] != '.'):
                raise WordPlacementConflict
            for i in range(len(word)):
                # If incoming letter doesn't match existing letter, bail out.
                if re.match(lines[y + i][x], word[i]) is None:
                    raise WordPlacementConflict
                # Check neighbouring columns. Bail out if there's something in them for words that aren't intersecting.
                for col_offset in [-1, 1]:
                    if dimensions[0] <= placement[0] + col_offset < dimensions[2]:
                        if lines[y + i][x + col_offset] != '.' and lines[y + i][x] == '.':
                            raise WordPlacementConflict
                # Increment numintersections if we're matching existing letter (ie. intersection)
                numintersections += lines[y + i][x] != '.'
                lines[y + i] = lines[y + i][:x] + word[i] + lines[y + i][x + 1:]
        if display:
            print('\n'.join(lines) + '\n')

    return (lines, numintersections, width * height)
