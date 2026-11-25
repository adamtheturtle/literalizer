module Main

let make_widget (_text: obj) : obj = null
type Val =
    | FStr of string
let my_data = make_widget(FStr "first \"quote\"\n// string body") // note
// extra
