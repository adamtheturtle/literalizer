module Main

let f (_a: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val array
f([|FInt 1L|]) |> ignore
