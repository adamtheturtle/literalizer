{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    positive: float
    negative: float
    nanValue: float
    finite: float
var my_data = Record0(
    positive: Inf,
    negative: -Inf,
    nanValue: NaN,
    finite: 1.5
)
