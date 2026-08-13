module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


deep : Val
deep = EList [
    EList [
        EInt 1,
        EInt 2
        ],
    EList [
        EInt 3,
        EInt 4
        ]
    ]
my_data : Val
my_data = EDict [
    ("a", EDict [
        ("b", EDict [
            ("c", deep)
            ])
        ])
    ]
