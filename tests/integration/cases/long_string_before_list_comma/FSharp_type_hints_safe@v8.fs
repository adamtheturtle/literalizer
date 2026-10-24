module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FStr "This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.";
    FInt 1L
]
