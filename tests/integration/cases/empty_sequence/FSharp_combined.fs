module Check

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let mutable my_data: Val = FList [
    FList [];
    FMap []
]
