module Main

type Val =
    | FInt of int64
    | FList of Val list
let f (_a: obj) : obj = null
let repr (__arg: obj) : obj = null
let ref_data: Val = FInt 1L
repr(f(ref_data)) |> ignore
