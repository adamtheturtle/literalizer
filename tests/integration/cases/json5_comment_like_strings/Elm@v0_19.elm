module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EStr "// data",
    EStr "/* data */",
    EStr "escaped quote: \" // data",
    EStr "backslash: \\"
    ]
