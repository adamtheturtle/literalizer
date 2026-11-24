module Main

let make_widget (_count: obj) : obj = null
type Val =
    | FInt of int64
let my_data = (
    if make_widget(FInt 42L) <> null then
        make_widget(FInt 42L) // inner
    else null
) // trailing
