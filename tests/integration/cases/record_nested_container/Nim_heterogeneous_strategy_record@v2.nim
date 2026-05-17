type Record0 = object
    title: string
    tags: seq[string]
    priority: int
var my_data = Record0(
    title: "report",
    tags: @[
        "draft",
        "urgent",
        "review"
    ],
    priority: 2
)
