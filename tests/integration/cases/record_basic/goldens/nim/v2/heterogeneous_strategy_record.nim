{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    id: int
    label: string
    enabled: bool
    relatedIds: seq[int]
var my_data = Record0(
    id: 1,
    label: "She said \"hello\", then waved",
    enabled: false,
    relatedIds: @[
        1,
        2,
        3
    ]
)
