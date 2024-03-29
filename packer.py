import random
from exceptions import WordPlacementConflict
from itertools import permutations

from constants import ACROSS, DOWN
from drawer import score_placements

CLUES = """
A ROARER  /  Lion sounds like light in the north. (1,6)
EURON GREYJOY  /  "You're on, dull girl!" - whispered the salty king. (5,7)
ASSUMING  /  Presumptuous sounds from a footwear dynasty. (8)
SOFT SERVE  /  Gentle delivery for 70c. (4,5)
TREASON  /  Naughty senator to go behind leader's back. (7)
ICHABOD  /  Enrich a body's shrouds for Eli's relative. (7)
THOR  /  God! That's a lispy boo boo. (4)
SCENTED  /  A kind of candle that's "in the middle". (7)
ORGAN  /  Citrus endlessly messed up a kidney. (5)
DOUBLE FREE  /  Too much deallocation, like 33. (6,4)
WOOL  /  Pull over! Eyes looking through two olives. (4)
FOREIGN  /  Alien flautist's obnoxious starts rule! (7)
BERU  /  Aunty sells german ignition parts for rideshare revolution. (4)
LAMBDA  /  Sign of Greek sheep expressing support in Russian. (6)
GIT  /  Clown show succeeds pioneering grin; get variant? (3)
PINNACLE  /  Salt-tolerant tree is lofty! (8)
GAIT  /  Sweating, having lost all direction; shaky step. (4)
POTASSIUM  /  K thanks, I will dose this marsupial.
TINTIN  /  Sn-sn-snowy's owner. (6)
LEOPARDSKIN  /  Unrefined alpine dorks spotted finery. (11)
DONCASTER  /  Half-assed mage spells birthed first Victorian tram. (9)
ARIADNE  /  Amazing mythological princess is just a headless Welsh darling. Not even headstrong... (7)
NABS  /  Seizes Australian banks. (4)
DOWN  /  Day to own up? Quite the opposite. (4)
DOOR  /  Gateway drug neglected underground? Has twice the love! (4)
TOAD  /  Tinkerbell, without further ado, conjured a leathery pest. (4)
SPEWS  /  Vomits sushi primarily behind church benches. (5)
SATIN  /  Glossed over the Great Australian Bight; OZ heartless. (5)
REACT  /  Respond rudely at rec meeting. (5)
KEYED  /  Scratched car in Kentucky Derby, I heard. (5)
WEANER  /  Crappy new era has stopped sucking. (6)
EMPTY  /  Tempt yourself to show how to make things clear. (5)
EDNA  /  Australian dame is perhaps Dane? (4)
DOGGO  /  Pupper reverses the almighty's advance. (5)
OAK  /  Tree professor. (3)
NAN  /  Granny not great with numbers. (3)
SLA  /  Contract instigating slaughter. (3)
NA  /  Continent shared by Batman and the Beatles. (2)
AIR  /  Lopped monster's hidey-hole. Jordin Sparks is not having it! (3)
MOAT  /  Surround the castle? Sounds like it's watering! (4)
BORK  /  Defamed Robert in a courthouse, or in Burger King. (4)
IDK  /  I'm uncertain about treating the child. (3)
"""

CLUE_DICT = {}
for clue in CLUES.splitlines():
    if not clue:
        continue
    word, hint = clue.split('  /  ')
    CLUE_DICT[word.replace(' ', '')] = (word, hint)

BEST_RESULTS = {
    'intersections': ([], 0),
    'area': ([], 10000),
}

GLOBALS = {
    'QUOTA': -1
}


def place_words(permutation, placements={}):
    if GLOBALS['QUOTA'] == 0:
        return
    if not permutation:
        GLOBALS['QUOTA'] -= 1
        try:
            lines, intersections, area = score_placements(placements)
            # print(placements)
            # print('\n'.join(lines) + f"\nSCORE: {intersections}/{BEST_RESULTS['intersections'][1]}, {area}/{BEST_RESULTS['area'][1]}\n")
            if intersections > BEST_RESULTS['intersections'][1]:
                print('\n'.join(lines) + f'\nSCORE: {intersections}, {area}\n')
                BEST_RESULTS['intersections'] = (lines, intersections)
            if area < BEST_RESULTS['area'][1]:
                print('\n'.join(lines) + f'\nSCORE: {intersections}, {area}\n')
                BEST_RESULTS['area'] = (lines, area)
        except WordPlacementConflict:
            pass
        return
    if len(placements) >= 2:
        # Run scoring to validate.
        try:
            score_placements(placements)
        except WordPlacementConflict:
            return
    curword = permutation[0]
    if not placements:
        place_words(permutation[1:], {**placements, curword: (0, 0, ACROSS)})
    else:
        for curi, curc in enumerate(curword):
            for word, placement in placements.items():
                for i, c in enumerate(word):
                    if c == curc:
                        if placement[2] == ACROSS:
                            place_words(permutation[1:], {**placements, curword: (placement[0] + i, placement[1] - curi, DOWN)})
                        else:
                            place_words(permutation[1:], {**placements, curword: (placement[0] - curi, placement[1] + i, ACROSS)})


# for permutation in permutations(sorted(CLUE_DICT.keys(), key=lambda w: -len(w))):
#     place_words(list(permutation))

permutation = list(CLUE_DICT.keys())
while True:
    GLOBALS['QUOTA'] = 300
    random.shuffle(permutation)
    place_words(permutation)
