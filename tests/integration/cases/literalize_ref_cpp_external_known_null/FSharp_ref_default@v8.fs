module Main

type Val =
    | FNull
    | FList of Val list
let consume_widget (__arg: obj) : obj = null
let item: Val = FNull
let my_data: Val = FNull
consume_widget(my_data) |> ignore
let my_data: Val = item
consume_widget(my_data) |> ignore
