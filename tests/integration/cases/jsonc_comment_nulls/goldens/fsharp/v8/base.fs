module Main

type Val =
    | FNull
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    // null heading
    // before null
    ("a", FNull);  // first null
    ("b", FNull)  // second null
]
