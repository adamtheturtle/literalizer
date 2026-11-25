module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "a_b" (PInt 0x1)),
    (Tuple "a-b" (PInt 0x2)),
    (Tuple "averyveryverylongkeynamethatgoesonandonandon" (PInt 0x3)),
    (Tuple "averyveryverylongkeynamethatgoesonandmore" (PInt 0x4))
]
