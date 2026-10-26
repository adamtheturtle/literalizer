module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FMap [("input", FMap [("name", FStr "alice"); ("city", FStr "paris")]); ("expected", FMap [("count", FInt 1L); ("total", FInt 2L)])];
    FMap [("input", FMap [("name", FInt 10L); ("city", FInt 20L)]); ("expected", FMap [("count", FStr "done"); ("total", FStr "pending")])]
]
