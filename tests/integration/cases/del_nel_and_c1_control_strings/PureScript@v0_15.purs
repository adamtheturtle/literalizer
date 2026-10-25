module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "del" (PStr "ab")),
    (Tuple "nel" (PStr "ab")),
    (Tuple "c1" (PStr "ab"))
]
