module Main

type Val =
    | FList of Val list
let make_widget (_value: obj) : obj = null
let items: Val = FList []
make_widget(items) |> ignore
