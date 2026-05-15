module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FMap [("call", FStr "send"); ("args", FList [FInt 1L; FStr "email"; FStr "a@gmail.com"; FInt 100L])];
    FMap [("call", FStr "recv"); ("args", FList [FInt 2L; FStr "sms"; FStr "b@example.com"; FInt 200L])]
]
