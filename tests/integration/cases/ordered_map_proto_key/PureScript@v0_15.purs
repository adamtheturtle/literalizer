module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "__proto__" (PDict [(Tuple "x" (PInt 1))])),
    (Tuple "ordinary" (PInt 2))
]
