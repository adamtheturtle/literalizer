module Main

type Val =
    | FInt of int64
    | FList of Val list
    | FDate of System.DateOnly
let ``process`` (_value: obj) : obj = null
let emit (__call: obj, __zip: obj) : obj = null
emit(``process``(FInt 1L), FDate (System.DateOnly(2024, 1, 15))) |> ignore
