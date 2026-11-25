module Main

type Val =
    | FInt of int64
let make_widget (_count: obj) : obj = null
let consume (_count: obj) : obj = null
do
    let mutable my_data = make_widget(FInt 7L)
    consume(my_data) |> ignore
    let my_data = (
        if make_widget(FInt 13L) <> null then
            make_widget(FInt 13L) // inner
        else null
    ) // trailing
    consume(my_data) |> ignore
    ()
