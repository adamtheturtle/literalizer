{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    dueDate: int
    parentId: int
    assignee: string
var my_data = @[
    Record0(dueDate: -1, parentId: -1, assignee: ""),
    Record0(dueDate: 10, parentId: 20, assignee: "alice")
]
