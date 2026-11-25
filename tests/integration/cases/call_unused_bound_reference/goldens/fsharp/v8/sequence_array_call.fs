module Main

let f (_value: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val array
f([|FInt 1L; FInt 2L|]) |> ignore
