import tables
{.warning[UnusedImport]:off.}
type Record0 = object
    x: int
var my_data = {
    "outer": @[{"inner": Record0(x: 1)}.toOrderedTable, {"inner": Record0(x: 2)}.toOrderedTable]
}.toOrderedTable
