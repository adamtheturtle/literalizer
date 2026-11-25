{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    nan: float
    positive: float
    negative: float
var std = Record0(
    nan: NaN,
    positive: Inf,
    negative: -Inf
)
