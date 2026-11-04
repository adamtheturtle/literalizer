module Main

let f (_a: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val array
f([|FList ([|FInt 1L; FInt 2L|]); FList ([|FInt 3L|])|]) |> ignore
