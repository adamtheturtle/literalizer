module Main

type Val =
    | FNull
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("nil", FList [FList [FList [FList [FList [FList [FList [FList [FList [FNull]]]]]]]]]);
    ("empty", FList [FList [FList [FList [FList [FList [FList [FList [FList [FList []]]]]]]]]]);
    ("siblings", FList [FList [FList [FList [FList [FList [FList [FList [FList [FList [FInt 4L; FInt 5L]]]]]]]]]])
]
