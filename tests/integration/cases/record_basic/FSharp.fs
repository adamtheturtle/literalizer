module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("id", FInt 1L);
    ("description", FStr "She said \"hello\", then waved");
    ("is_done", FBool false);
    ("blocks", FList [FInt 1L; FInt 2L; FInt 3L])
]
