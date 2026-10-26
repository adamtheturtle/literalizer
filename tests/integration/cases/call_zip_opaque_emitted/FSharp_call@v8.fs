module Main

type Val =
    | FInt of int64
    | FList of Val list
    | FDatetime of System.DateTime
let ``process`` (_value: obj) : obj = null
let emit (__call: obj, __zip: obj) : obj = null
emit(``process``(FInt 1L), FDatetime (System.DateTime(2024, 1, 15, 12, 0, 0))) |> ignore
