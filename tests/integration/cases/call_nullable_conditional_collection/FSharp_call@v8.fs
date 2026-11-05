module Main

let make_widget (_count: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
let my_data = (
    if make_widget(FList [FInt 1L; FInt 2L]) <> null then
        make_widget(FList [FInt 1L; FInt 2L]) // inner
    else null
) // trailing
