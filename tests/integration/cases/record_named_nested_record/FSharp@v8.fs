module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("collection", FStr "alpha");
    ("featured_entry", FMap [("id", FInt 100L); ("label", FStr "first entry"); ("enabled", FBool false); ("related_ids", FList [FInt 102L; FInt 103L])])
]
