module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


my_data : Val
my_data = EList [
    EList [
        EList [],
        EList []
        ],
    EList [
        EList [],
        EList [
            EInt 1
            ]
        ]
    ]
