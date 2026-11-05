# Traffic jam model: ODD

Cars on a ring road, after Nagel and Schreckenberg (1992). The structure is the
ODD protocol (Grimm et al. 2020). Each submodel in section 7 says which function
of `model.py` it is.

## 1. Purpose and patterns

**Question:** Can a traffic jam appear with no accident, no road work and no
traffic light?

- **A jam from nothing:** with enough cars and a little random slowing down, a
  cluster of standing cars appears on a road that was running freely.
- **A jam that travels backwards:** the jam moves against the direction in which
  the cars drive, although every car drives forwards.
- **Density matters:** with few cars the road stays free, with more cars the
  average speed drops.

## 2. Entities, state variables and scales

**Entities:** cars (the agents) on a one-dimensional ring road. The road is a ring of
cells, so a car that leaves the last cell comes back in the first.

**State variables of a car:**

- `position`: the cell the car is in, a whole number
- `speed`: cells per step, a whole number from 0 to `V_MAX`

**State variables of the road:**

- `length`: the number of cells (`LENGTH = 100`)
- `dawdle_chance`: the chance that a car slows down by one, 0 to 1

**Scales:** one cell is 7.5 m (about one car and a gap), one step is 1 second, so
the top speed `V_MAX = 5` cells per step is 135 km/h. The road is 750 m long.
Runs are a few hundred steps.

## 3. Process overview and scheduling

One process: **driving**. In every step all cars, in the order of the ring:

1. work out the speed for the coming step, by the three speed rules (accelerate,
   brake, dawdle), using the road as it is at the start of the step,
2. then **all** cars move by their new speed.

All cars change at the same time (a synchronous update): the speed of a car
never depends on another car that has already moved in this step.

## 4. Design concepts

The eleven design concepts, each with what it means in this model:

- **Basic principles:** traffic as many cars that only look at the car in front.
- **Emergence:** the jam. No car is told to stop and none is told where the jam
  goes. It comes from density, the rules and the random slowing down.
- **Adaptation:** a car adapts its speed to the gap in front of it.
- **Objectives:** implicit. Drive as fast as allowed without hitting the car in
  front.
- **Learning:** none.
- **Prediction:** none, a car reacts to the gap it has now.
- **Sensing:** a car knows the gap to the car directly in front of it, nothing
  else.
- **Interaction:** indirect. A car that brakes shortens the gap of the car behind
  it.
- **Stochasticity:** each car dawdles with chance `dawdle_chance` in each step:
  human imperfection.
- **Collectives:** none.
- **Observation:** the space-time diagram (one row per step), the average speed,
  the number of standing cars.

## 5. Initialization

`count` cars, evenly spread over the ring, all standing still. The random numbers
come from one generator that can be given a seed, so that a run can be repeated.

## 6. Input data

None. The road is the same everywhere and nothing comes from outside.

## 7. Submodels

Each car applies these four, in this order, with its own `speed` and the `gap` in
front of it (the empty cells up to the next car).

1. **Accelerate:** one faster, up to the top speed.
   - Rule: `speed = min(speed + 1, V_MAX)`
   - In the code: `accelerate`
2. **Brake:** never further than the empty cells in front.
   - Rule: `speed = min(speed, gap)`
   - In the code: `brake`
3. **Dawdle:** with chance `dawdle_chance`, and only if `speed > 0`, one slower.
   - Rule: `speed = speed - 1`
   - In the code: `dawdle`
4. **Move:** all cars at once, and a car that leaves the last cell comes back in
   the first.
   - Rule: `position = (position + speed) % length`
   - In the code: `step`

Rules 1 to 3 give the new speed, rule 4 moves the cars. Rules 1 to 3 use the gaps
from the start of the step.

## References

- Nagel, K., Schreckenberg, M. (1992). A cellular automaton model for freeway
  traffic. *Journal de Physique I* 2(12), 2221-2229.
- Sugiyama, Y. et al. (2008). Traffic jams without bottlenecks: experimental
  evidence for the physical mechanism of the formation of a jam. *New Journal of
  Physics* 10, 033001.
- Grimm, V. et al. (2020). The ODD protocol for describing agent-based and other
  simulation models: a second update. *JASSS* 23(2), 7.
