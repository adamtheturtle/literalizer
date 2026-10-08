{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    a: seq[seq[int]]
    b: seq[seq[int]]
var my_data = Record0(
    a: @[
        @[
            1,
            2
        ],
        @[
            3
        ]
    ],
    b: @[
        @[],
        @[
            1
        ]
    ]
)
