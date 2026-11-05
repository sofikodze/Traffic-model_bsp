"""Cars on a ring road: the Nagel-Schreckenberg traffic model.

ODD.md describes the model. Each submodel there is one function here, in the
same order. All of them are done but `brake`, which is yours: for now it hands
the speed back unchanged, so the model already runs, but no car looks at the
road in front of it, and cars drive through each other.

Run this file and it prints the road as text: one line per step, a digit is the
speed of a car, a dot an empty cell. A jam is a slanting stripe of 0s. It runs
200 steps, so that a jam has time to appear, and prints the last 40.

    uv run python model.py              # 20 cars, 30% dawdling
    uv run python model.py 12 0.1       # 12 cars, 10% dawdling
"""

import random
import sys
from dataclasses import dataclass

LENGTH = 100  # cells of the ring road
V_MAX = 5  # top speed, in cells per step


# ODD 2: the entities and their state variables
@dataclass
class Car:
    position: int  # the cell the car is in, 0 to LENGTH - 1
    speed: int = 0  # cells per step


@dataclass
class Road:
    cars: list[Car]  # in the order of the ring: the next car is the car in front
    length: int = LENGTH
    dawdle_chance: float = 0.3


# ODD 5: initialization
def new_road(count: int, dawdle_chance: float = 0.3, length: int = LENGTH) -> Road:
    """`count` cars, evenly spread over the ring and standing still."""
    cars = [Car(position=i * length // count) for i in range(count)]
    return Road(cars, length, dawdle_chance)


# ODD 4, sensing: what a car knows
def gap(road: Road, i: int) -> int:
    """The empty cells in front of car `i`, up to the next car."""
    cars = road.cars
    if len(cars) == 1:
        return road.length - 1
    ahead = cars[(i + 1) % len(cars)]
    return (ahead.position - cars[i].position - 1) % road.length


# ODD 7, submodel 1
def accelerate(speed: int) -> int:
    """A car that is not at the top speed gets one faster."""
    return min(speed + 1, V_MAX)


# ODD 7, submodel 2
def brake(speed: int, gap: int) -> int:
    """A car never goes further than the empty cells in front of it."""
    # TODO: the rule of ODD 7. For now the car ignores the gap.
    return speed


# ODD 7, submodel 3
def dawdle(speed: int, chance: float, rng: random.Random) -> int:
    """With the chance `chance`, a car that is moving gets one slower.

    `rng.random()` gives a number from 0 up to (not including) 1, so it is
    smaller than `chance` with the chance `chance`.
    """
    if speed > 0 and rng.random() < chance:
        return speed - 1
    return speed


# ODD 3 and 7, submodel 4
def step(road: Road, rng: random.Random) -> None:
    """One step for all cars at once. Changes the road.

    Every car first gets its new speed (accelerate, brake, dawdle), using the
    gaps as they are at the start of the step. Only then do all cars move.
    """
    gaps = [gap(road, i) for i in range(len(road.cars))]
    for i, car in enumerate(road.cars):
        gap_ahead = gaps[i]
        car.speed = accelerate(car.speed)
        car.speed = brake(car.speed, gap_ahead)
        car.speed = dawdle(car.speed, road.dawdle_chance, rng)
    for car in road.cars:
        car.position = (car.position + car.speed) % road.length


# ODD 4, observation
def row(road: Road) -> list[int]:
    """The speed in the cell of each car and -1 in an empty cell: one row of the
    space-time diagram."""
    cells = [-1] * road.length
    for car in road.cars:
        cells[car.position] = car.speed
    return cells


def simulate(
    count: int, dawdle_chance: float, steps: int, seed: int | None = None
) -> list[list[int]]:
    """Runs a new road for `steps` steps and gives the rows of every step."""
    rng = random.Random(seed)
    road = new_road(count, dawdle_chance)
    rows = [row(road)]
    for _ in range(steps):
        step(road, rng)
        rows.append(row(road))
    return rows


# What happens when you run the file: uv run python model.py
if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    chance = float(sys.argv[2]) if len(sys.argv) > 2 else 0.3

    rows = simulate(count, chance, steps=200, seed=1)[-40:]
    for cells in rows:
        print("".join("." if v < 0 else str(v) for v in cells))

    speeds = [v for cells in rows for v in cells if v >= 0]
    average = sum(speeds) / len(speeds)
    standing = speeds.count(0) / len(rows)
    print(f"{count} cars, {chance:.0%} dawdling: average speed {average:.1f}")
    print(f"cars standing per step: {standing:.1f}")
