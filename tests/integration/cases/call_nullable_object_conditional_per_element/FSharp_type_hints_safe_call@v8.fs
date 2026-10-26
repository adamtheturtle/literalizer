module Main

let make_widget (_count: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
let my_data = (
    if make_widget(FInt 7L) <> null then
        make_widget(FInt 7L) // inner
    else null
) // trailing
