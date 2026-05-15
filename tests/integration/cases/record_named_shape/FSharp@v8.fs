module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FMap [("id", FInt 100L); ("description", FStr "first task"); ("is_done", FBool false); ("blocks", FList [FInt 102L; FInt 103L])];
    FMap [("id", FInt 101L); ("description", FStr "second task"); ("is_done", FBool true); ("blocks", FList [])]
]
