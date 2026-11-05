import tables
{.warning[UnusedImport]:off.}
type Record0 = object
    replacement: int
    present: int
var my_data = {
    "rows": @[Record0(replacement: -1, present: 1), Record0(replacement: 2, present: 3)]
}.toOrderedTable
