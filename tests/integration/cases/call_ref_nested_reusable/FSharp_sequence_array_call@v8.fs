module Main

type Val =
    | FInt of int64
    | FList of Val array
let ``process`` (_data: obj) : obj = null
let item: Val array = [|
    FInt 1L;
    FInt 2L
|]
``process``([|FList (item); FList (item)|]) |> ignore
