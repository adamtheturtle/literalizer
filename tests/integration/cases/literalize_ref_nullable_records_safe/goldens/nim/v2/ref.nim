{.warning[UnusedImport]:off.}
import tables
type Record1 = object
    x: int
    y: pointer
type Record2 = object
    x: pointer
    y: pointer
type Record3 = object
    x: int
    y: int
type Record0 = object
    nullable: Record1
    nullFields: Record2
    plain: Record3
var nullable = Record1(
    x: 1,
    y: nil
)
var nullFields = Record2(
    x: nil,
    y: nil
)
var plain = Record3(
    x: 1,
    y: 2
)
var my_data = Record0(
    nullable: nullable,
    nullFields: nullFields,
    plain: plain
)
