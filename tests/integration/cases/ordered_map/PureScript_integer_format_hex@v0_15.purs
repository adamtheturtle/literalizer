module Check where


data Tuple a b = Tuple a b
data Val
    = PBool Boolean
    | PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "name" (PStr "Alice")),
    (Tuple "age" (PInt 0x1e)),
    (Tuple "active" (PBool true))
]
