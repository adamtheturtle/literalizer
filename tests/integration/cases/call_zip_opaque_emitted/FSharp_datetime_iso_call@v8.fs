module Main

type Val =
    | FInt of int64
    | FList of Val list
    | FStr of string
let ``process`` (_value: obj) : obj = null
let emit (__call: obj, __zip: obj) : obj = null
emit(``process``(FInt 1L), FStr "2024-01-15T12:00:00") |> ignore
