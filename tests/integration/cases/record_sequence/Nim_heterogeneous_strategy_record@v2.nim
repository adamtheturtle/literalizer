{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    id: int
    label: string
    tags: seq[string]
var my_data = @[
    Record0(id: 1, label: "first", tags: newSeq[string]()),
    Record0(id: 2, label: "second", tags: newSeq[string]()),
    Record0(id: 3, label: "third", tags: newSeq[string]())
]
