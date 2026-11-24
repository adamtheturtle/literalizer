{.warning[UnusedImport]:off.}
import tables
type Record0 = object
    a: int
    b: string

let my_data = @[Record0(
    a: 1,
    b: "x"
)]
discard my_data
