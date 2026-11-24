module Main

type Val =
    | FInt of int64
let make_widget (_count: obj) : obj = null
let consume (_count: obj) : obj = null
do
    let mutable my_data = make_widget(FInt 42L)
    consume(my_data) |> ignore
    let my_data = make_widget(FInt 42L) // note
    // extra
    consume(my_data) |> ignore
    ()
