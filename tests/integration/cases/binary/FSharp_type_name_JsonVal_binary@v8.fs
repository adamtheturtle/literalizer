module Main

type JsonVal =
    | FStr of string
    | FList of JsonVal list
let my_data: JsonVal = FList [
    FStr "48656c6c6f"
]
