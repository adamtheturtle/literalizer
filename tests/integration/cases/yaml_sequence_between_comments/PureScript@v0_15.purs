module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PDict [(Tuple "item" (PStr "existing"))],
    -- This comment describes the next item.
    PDict [(Tuple "item" (PStr "next"))]
    ]
