module Main

type Val =
    | FNull
    | FInt of int64
    | FList of Val array
let ``process`` (_value: obj) : obj = null
``process``(FNull) |> ignore
``process``([|FInt 1L; FInt 2L|]) |> ignore
