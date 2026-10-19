{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    flags: seq[bool]
    values: seq[float]
    ints: seq[int]
    text: seq[string]
    nestedFlags: seq[seq[bool]]
    nestedValues: seq[seq[float]]
var my_data = Record0(
    flags: @[
        true,
        false
    ],
    values: @[
        1.5,
        -2.25
    ],
    ints: @[
        1,
        2
    ],
    text: @[
        "a"
    ],
    nestedFlags: @[
        @[
            true
        ],
        @[
            false
        ]
    ],
    nestedValues: @[
        @[
            1.5
        ],
        @[
            2.25
        ]
    ]
)
