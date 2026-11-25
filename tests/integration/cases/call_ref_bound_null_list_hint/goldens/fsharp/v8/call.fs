module Main

type Val =
    | FNull
    | FInt of int64
    | FList of Val list
let consume (_value: obj) : obj = null
let item: Val = FNull
consume(item) |> ignore
