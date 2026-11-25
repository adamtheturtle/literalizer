module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


deep : Val
deep = EList [
    EList [
        EStr "one",
        EStr "two"
        ],
    EList [
        EStr "three",
        EStr "four"
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
