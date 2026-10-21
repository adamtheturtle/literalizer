module Main

type Val =
    | FNull
let consume (_value: obj) : obj = null
let item: Val = FNull
consume(item) |> ignore
