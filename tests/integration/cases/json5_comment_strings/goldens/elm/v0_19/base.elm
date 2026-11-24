module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    -- strings stay data
    EStr "https://example.org/a/*b*/",  -- URL annotation
    EStr "escaped quote: \" // still data",
    EStr "backslash: \\",  -- outside the string
    EStr "/* not a comment */"
    ]
