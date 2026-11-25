import tables
{.warning[UnusedImport]:off.}
type Record0 = object
    name: pointer
    id: int
var my_data = {
    "outer": @[Record0(name: nil, id: 1)]
}.toOrderedTable
