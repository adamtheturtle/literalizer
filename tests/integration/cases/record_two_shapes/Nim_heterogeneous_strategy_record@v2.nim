{.warning[UnusedImport]:off.}
import tables
type Record1 = object
    count: int
    rate: int
type Record2 = object
    retries: int
    timeout: int
type Record0 = object
    metrics: Record1
    flags: Record2
var my_data = Record0(
    metrics: Record1(
        count: 100,
        rate: 50
    ),
    flags: Record2(
        retries: 3,
        timeout: 30
    )
)
