module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PList [
        PDict [(Tuple "item" (PStr "existing"))],
        PStr "kept"
        -- This comment trails the first pair.
        ],
    PList [PDict [(Tuple "item" (PStr "next"))], PStr "also kept"],
    -- This comment describes the last pair.
    PList [PDict [(Tuple "item" (PStr "last"))], PStr "kept too"]
    ]
