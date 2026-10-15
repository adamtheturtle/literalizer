module Check exposing (..)


type Val
    = EList (List Val)


my_data : Val
my_data = EList [
    -- outer heading
    -- first empty
    EList [],
    -- second empty
    EList []
    ]
