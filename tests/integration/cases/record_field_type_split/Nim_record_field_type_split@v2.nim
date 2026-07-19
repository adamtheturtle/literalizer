{.warning[UnusedImport]:off.}
import tables
type Record1 = object
    status: int
type Record2 = object
    status: string
type Record4 = object
    kind: string
    urgent: bool
type Record3 = object
    inner: Record4
type Record6 = object
    error: string
type Record5 = object
    inner: Record6
type Record7 = object
    holder: Record1
type Record8 = object
    holder: Record2
type Record9 = object
    nums: seq[int]
type Record0 = object
    plain: Record1
    other: Record2
    nestedA: Record3
    nestedB: Record5
    wrapA: Record7
    wrapB: Record8
    wide: Record9
var my_data = Record0(
    plain: Record1(
        status: 1
    ),
    other: Record2(
        status: "ready"
    ),
    nestedA: Record3(
        inner: Record4(
            kind: "add",
            urgent: true
        )
    ),
    nestedB: Record5(
        inner: Record6(
            error: "not_found"
        )
    ),
    wrapA: Record7(
        holder: Record1(
            status: 2
        )
    ),
    wrapB: Record8(
        holder: Record2(
            status: "word"
        )
    ),
    wide: Record9(
        nums: @[
            1,
            1099511627776
        ]
    )
)
