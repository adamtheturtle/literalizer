type Record1 = object
    id: int
    label: string
type Record0 = object
    name: string
    items: seq[Record1]
var my_data = Record0(
    name: "box",
    items: @[
        Record1(
            id: 1,
            label: "first"
        ),
        Record1(
            id: 2,
            label: "second"
        )
    ]
)
