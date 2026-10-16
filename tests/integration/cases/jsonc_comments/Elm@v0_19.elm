module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    -- A JSONC input case with both comment forms.
    ("url", EStr "https://example.org/a/*b*/"),  -- detail
    -- continued
    ("count", EInt 2)  -- trailing line comment
    ]
