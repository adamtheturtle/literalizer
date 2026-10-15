module Main

type Val =
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FStr "// data";
    FStr "/* data */";
    FStr "escaped quote: \" // data";
    FStr "backslash: \\"
]
