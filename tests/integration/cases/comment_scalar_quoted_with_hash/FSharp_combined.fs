module Check

type Val =
    | FStr of string
// note
let mutable my_data: Val = FStr "hello # world"
