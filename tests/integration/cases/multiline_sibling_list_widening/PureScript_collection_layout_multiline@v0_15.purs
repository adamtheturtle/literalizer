module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "omap_value" (PDict [
        (Tuple "first" (PInt 1))
        ])),
    (Tuple "sibling_lists" (PDict [
        (Tuple "numbers" (PList [
            PInt 1,
            PInt 2
            ])),
        (Tuple "strings" (PList [
            PStr "x",
            PStr "y"
            ]))
        ])),
    (Tuple "ref_marker_present" (PList [
        PStr "$keep",
        PStr "z"
        ]))
    ]
