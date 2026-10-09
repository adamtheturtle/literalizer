{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    numbers: seq[int]
    nestedNumbers: seq[seq[int]]
    words: seq[string]
    flag: bool
var my_data = Record0(
    numbers: @[
        1,
        2
    ],
    nestedNumbers: @[
        @[
            3,
            4
        ],
        @[
            5,
            6
        ]
    ],
    words: @[
        "s"
    ],
    flag: true
)
