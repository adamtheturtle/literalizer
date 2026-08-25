{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    value: int
var my_data = Record0(
    value: cast[int](0o1000000000000000000000'u64)
)
