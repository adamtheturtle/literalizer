module Check

type Val =
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FStr "C:\\path\\to\\file";
    FStr "back\\\\slash";
    FStr "hello \\\"world\\\""
]
