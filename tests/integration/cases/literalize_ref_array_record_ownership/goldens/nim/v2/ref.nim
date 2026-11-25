{.warning[UnusedImport]:off.}
import tables
type Record1 = object
    values: seq[int]
type Record2 = object
    nested: seq[seq[int]]
type Record0 = object
    trivial: Record1
    nested: Record2
var trivial = Record1(
    values: @[
        1,
        2
    ]
)
var nested = Record2(
    nested: @[
        @[
            1,
            2
        ],
        @[
            3,
            4
        ]
    ]
)
var my_data = Record0(
    trivial: trivial,
    nested: nested
)
