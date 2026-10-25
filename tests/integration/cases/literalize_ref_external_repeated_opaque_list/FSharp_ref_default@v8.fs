module Main

type Val =
    | FList of Val list
let consume_widget (_arg_value: obj) : obj = null
let item: Val = FList []
let my_data: Val = FList [
    item;
    item
]
consume_widget(my_data) |> ignore
