import json
var deep = %* [
    [
        1,
        2
    ],
    [
        3,
        4
    ]
]
var my_data = %* {
    "a": {
        "b": {
            "c": deep
        }
    }
}
