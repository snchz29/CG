PRESETS = [
    [[i / 1000, (1 - (i / 1000) ** 2) ** (1 / 2)] for i in range(-1000, 1001)],
    [
        [-2 / 3, 1, -2 / 3, -1],
        [2 / 3, 1, 2 / 3, -1],
        [-1, -2 / 3, 1, -2 / 3],
        [-1, 2 / 3, 1, 2 / 3],
    ],
    [
        [0, 0],
        [1 / 3, 0],
        [1 / 3, 1 / 3],
        [-1 / 3, 1 / 3],
        [-1 / 3, -1 / 3],
        [2 / 3, -1 / 3],
        [2 / 3, 2 / 3],
        [-2 / 3, 2 / 3],
        [-2 / 3, -2 / 3],
        [1, -2 / 3],
        [1, 1],
        [-1, 1],
        [-1, -1],
        [1, -1]
    ],
    [
        [0, 1],
        [.25, .5],
        [.75, .75],
        [.5, .25],
        [1, 0],
        [.5, -.25],
        [.75, -.75],
        [.25, -.5],
        [0, -1],
        [-.25, -.5],
        [-.75, -.75],
        [-.5, -.25],
        [-1, 0],
        [-.5, .25],
        [-.75, .75],
        [-.25, .5],
    ],
    [
        [0, 1, 1, -.5, -1, -.5],
        [0, -1, 1, .5, -1, .5],
    ],
    [
        [0, -1, -1, -1, -.5, -.5],
        [0, 1],
        [.5, -.5],
        [1, -1],
    ],
    [
        [0, -1, -1, -1, -.5, -.5],
        [0, 1],
        [.5, -.5],
        [1, -1],
    ],
    [
        [-1, 1, -1, .25, -.25, .25, -.25, 1],
        [1, 1, 1, .25, .25, .25, .25, 1],
        [-1, -1, -1, -.25, -.25, -.25, -.25, -1],
        [1, -1, 1, -.25, .25, -.25, .25, -1],
        [-.75, .75, -.75, -.75, .75, -.75, .75, .75],
    ],
    [
        [-1, -.25, -1, .25, -.5, -.75, -.5, .75],
        [.5, -.75, .5, .75],
        [0, -.25, 0, .25],
        [1, -.5, 1, .5],
    ],
    [[i / 100, (1 - (i / 100) ** 2) ** (1 / 2)] for i in range(-100, 101)],
]
