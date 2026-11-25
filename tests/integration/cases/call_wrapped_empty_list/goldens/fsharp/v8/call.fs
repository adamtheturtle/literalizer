module Main

let make_widget (_value: obj) : obj = null
type Val =
    | FList of Val list
make_widget(FList []) |> ignore
