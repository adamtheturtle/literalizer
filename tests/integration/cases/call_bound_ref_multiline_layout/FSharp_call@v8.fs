module Main

type Val =
    | FInt of int64
    | FList of Val list
let f (_value: obj) : obj = null
let ref_data: Val = FList [
    FList [
        FInt 1L;
        FInt 2L
    ];
    FList [
        FInt 3L;
        FInt 4L
    ]
]
f(FList [
    FList [
        ref_data
    ]
])
