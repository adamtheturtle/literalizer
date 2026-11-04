{.warning[UnusedImport]:off.}
import tables
type Record1 = object
    age: int
type Record0 = object
    name: string
    active: bool
    count: int
    score: float
    missing: pointer
    scores: seq[int]
    child: Record1
var my_data = @[
    Record0(name: "Ada", active: true, count: 1, score: 1.5, missing: nil, scores: @[1, 2], child: Record1(age: 3)),
    Record0(name: "Bob", active: false, count: 2, score: 2.5, missing: nil, scores: @[4], child: Record1(age: 5))
]
