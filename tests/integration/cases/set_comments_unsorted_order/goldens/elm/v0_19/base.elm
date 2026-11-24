module Check exposing (..)


type Val
    = EStr String
    | ESet (List Val)


my_data : Val
my_data = ESet [
    -- before apple
    EStr "apple",
    EStr "banana"  -- banana inline
    -- trailing
    ]
