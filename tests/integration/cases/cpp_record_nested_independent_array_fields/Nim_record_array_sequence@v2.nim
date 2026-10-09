{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    numbers: seq[seq[int]]
    words: seq[seq[string]]
var my_data = Record0(
    numbers: @[
        @[
            1
        ],
        @[
            2
        ]
    ],
    words: @[
        @[
            "s"
        ],
        @[
            "t"
        ]
    ]
)
