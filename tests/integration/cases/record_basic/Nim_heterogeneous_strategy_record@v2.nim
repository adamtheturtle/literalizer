type Record0 = object
    id: int
    description: string
    isDone: bool
    blocks: seq[int]
var my_data = Record0(
    id: 1,
    description: "She said \"hello\", then waved",
    isDone: false,
    blocks: @[
        1,
        2,
        3
    ]
)
