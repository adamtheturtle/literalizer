module Main

type Val =
    | FInt of int64
let make_widget (_count: obj) : obj = null
let consume_widget (_count: obj) : obj = null
do
    let mutable my_data = make_widget(FInt 42L)
    consume_widget(my_data) |> ignore
    let my_data = make_widget(my_data) // note
    consume_widget(my_data) |> ignore
    ()
