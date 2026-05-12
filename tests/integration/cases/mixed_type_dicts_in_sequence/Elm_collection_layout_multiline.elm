module Check exposing (..)


type Val
    = EBool Bool
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [
        ("type", EStr "create"),
        ("pr_id", EStr "pr_1"),
        ("draft", EBool True)
        ],
    EDict [
        ("type", EStr "create"),
        ("pr_id", EStr "pr_2")
        ]
    ]
