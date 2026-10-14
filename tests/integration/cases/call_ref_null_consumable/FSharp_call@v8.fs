module Main

type Val =
    | FNull
    | FList of Val list
let consume (_value: obj) : obj = null
let my_null: Val = FNull
let regular_null: Val = FNull
consume(my_null) |> ignore
consume(regular_null) |> ignore
