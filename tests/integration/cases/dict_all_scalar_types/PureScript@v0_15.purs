module Check where


data Tuple a b = Tuple a b
data Val
    = PNull
    | PBool Boolean
    | PInt Int
    | PFloat Number
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "s" (PStr "string")),
    (Tuple "i" (PInt 1)),
    (Tuple "f" (PFloat 1.5)),
    (Tuple "b" (PBool true)),
    (Tuple "n" (PNull)),
    (Tuple "d" (PStr "2024-01-15")),
    (Tuple "dt" (PStr "2024-01-15T12:00:00")),
    (Tuple "by" (PStr "48656c6c6f"))
    ]
