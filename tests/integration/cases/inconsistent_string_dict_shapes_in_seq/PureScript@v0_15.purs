module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PDict [(Tuple "first" (PStr "Alice")), (Tuple "last" (PStr "Smith"))],
    PDict [(Tuple "first" (PStr "Bob")), (Tuple "middle" (PStr "Quincy"))]
    ]
