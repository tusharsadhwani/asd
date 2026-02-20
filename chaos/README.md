# chaos

One shotted by claude.

Prompt:

```text
I want to setup a p5js sketch that does the following:
- waits for first mouse click, does nothing by default
- on first click, starts drawing a line from where you clicked to the moust position
- on second click, stores the two points as the base line to draw, and then draws a line from the second point to the current position of the mouse. now, notice that the second line is basically a scaled version of the first line, with a different scale and angle. draw, fractal-style, 10 lines going off of the end of the previous line while multiplying the length factor and adding the angle.
```
