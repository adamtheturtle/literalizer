module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    // Server configuration
    ("host", FStr "localhost");  // default host
    ("port", FInt 8080L);
    // Enable debug mode
    ("debug", FBool true)
]
