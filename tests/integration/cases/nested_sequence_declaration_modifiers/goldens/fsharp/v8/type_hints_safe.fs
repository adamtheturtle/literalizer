module Main

type Val =
    | FNull
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FList [];
    FList [FInt 1L];
    FList [FInt 1L; FInt 2L];
    FList [FInt 1L; FStr "x"; FBool true; FNull];
    FList [FInt 1L; FInt 2L; FInt 3L; FInt 4L; FInt 5L; FInt 6L; FInt 7L; FInt 8L]
]
