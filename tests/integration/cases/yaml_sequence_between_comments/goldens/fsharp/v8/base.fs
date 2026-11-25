module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FMap [("item", FStr "existing")];
    // This comment describes the next item.
    FMap [("item", FStr "next")]
]
