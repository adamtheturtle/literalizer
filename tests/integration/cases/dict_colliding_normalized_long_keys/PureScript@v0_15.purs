module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "a_b" (PInt 1)),
    (Tuple "a-b" (PInt 2)),
    (Tuple "averyveryverylongkeynamethatgoesonandonandon" (PInt 3)),
    (Tuple "averyveryverylongkeynamethatgoesonandmore" (PInt 4))
    ]
