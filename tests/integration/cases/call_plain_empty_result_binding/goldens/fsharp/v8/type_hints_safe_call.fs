module Main

let make_widget (_value: obj) : obj = null
type Val =
    | FList of Val list
let my_data = make_widget(FList [])
