import tables
{.warning[UnusedImport]:off.}
type Record0 = object
    x: int
var my_data = @[
    {"first": Record0(x: 1)}.toOrderedTable,
    {"first": Record0(x: 2)}.toOrderedTable
]
