module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    // About the first dotted key.
    // About the second dotted key.
    ("dotted", FMap [("first", FInt 1L); ("second", FInt 2L)]);
    ("plain", FInt 3L);  // About the plain key.
    // Inside the table.
    ("table", FMap [("inner", FInt 4L)]);
    // Before the first entry.
    // Before the second entry.
    ("entries", FList [FMap [("name", FStr "one")]; FMap [("name", FStr "two")]])
]
