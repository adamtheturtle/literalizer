{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    x: int
var emptyItems = seq[Record0](@[])
var populatedItems = @[
    Record0(x: 1)
]
var my_data = @[
    emptyItems,
    populatedItems
]
