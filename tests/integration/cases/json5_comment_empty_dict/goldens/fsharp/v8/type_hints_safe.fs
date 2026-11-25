module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
// empty heading
// empty body
// after empty
let my_data: Val = FMap []
