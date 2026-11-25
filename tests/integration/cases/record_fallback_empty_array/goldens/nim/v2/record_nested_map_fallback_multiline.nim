{.warning[UnusedImport]:off.}
import tables
type
  ValueKind = enum
    vkInt, vkList
  Value = object
    case kind: ValueKind
    of vkInt: intVal: int
    of vkList: listVal: seq[Value]
type Record0 = object
    name: string
    payload: Table[string, Value]
var my_data = @[
    Record0(
        name: "one",
        payload: {
            "scalar": Value(kind: vkInt, intVal: 1),
            "items": Value(kind: vkList, listVal: newSeq[Value]())
        }.toTable
    ),
    Record0(
        name: "two",
        payload: {
            "other": Value(kind: vkInt, intVal: 2)
        }.toTable
    )
]
