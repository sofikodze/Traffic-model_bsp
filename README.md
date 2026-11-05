# Traffic jam model

Cars on a ring road. Nobody is told to stop, and still a jam appears and travels
backwards. This is the traffic model of the course *Applied Systems Sciences 1*:
`ODD.md` describes it, this repository is the code.

## Set up

```sh
uv sync                   # once: installs Python in .venv
uv run python model.py    # prints the road
```

## What is where

- `ODD.md`: the model in words, its purpose, entities and rules (section 7 has
  the rules).
- `model.py`: the model in code, one function for each submodel of the ODD.
  Run it and it prints the road as text, one line per step.

## Your tasks

1. **Look at it.** `uv run python model.py` prints 40 steps of the road: a digit
   is the speed of a car, a dot an empty cell. Right now `brake` in `model.py`
   hands the speed back unchanged: the cars drive at 4 or 5 and through each
   other, and two cars in one cell show as one digit.
2. **Brake.** Fill in `brake` with the rule of ODD section 7 and run `model.py`
   again. What changed, and why? Find the jam: a slanting stripe of 0s.
3. **Ask a question.** At what number of cars does the jam start? Does it start
   without dawdling? Try `uv run python model.py 12 0.1` (12 cars, 10%
   dawdling) and `uv run python model.py 20 0` (no dawdling), change the numbers
   and write down what you find. Then a speed limit: set `V_MAX` in `model.py`
   to 3 (81 km/h). Are there fewer standing cars? Is the average speed much
   lower?

Commit after every step that works, and push.
