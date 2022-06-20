
## Project Plan
- [X] Decide on renderer: pygame vs p5.py: pygame
- [X] Given initial conditions, detect time loops / oscillations
    - how many trips until the loop starts?
    - how many trips make up the oscillation loop?
- [X] Write fast-detect mode that skips render and stops once it detects a time loop
- [x] Write data collection script to answer early questions
    - [x] parallelization
    - [x] fancy progress bar
    - [x] save data as it goes
    - [x] resume

## Open Questions
1. How often do perfect time loops happen?
2. How often to time oscillations happen?
3. Do these vary based on the rule?
    1. yes! some rules are "dead" universes where nothing changes
    2. interesting, chaotic rules are: 161, 126, 165, 135, 73, 109, 18, 149, 86, 22, 151, 183, 90, 30
    3. I'm going to zoom in on a few: 30, 45, 73, 97, 110, 137, 161, 165, 169] that show a good diversity of behavior
4. Do these vary based on the portal size?
5. Do these vary based on the portal time / distance?


## Installation
```
sudo apt-get install libglfw3  # for pygame
sudo pip3 install -r requirements.txt
```
