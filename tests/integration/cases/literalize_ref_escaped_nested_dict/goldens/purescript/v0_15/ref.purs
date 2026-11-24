module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


existing :: Val
existing = PInt 1
my_data :: Val
my_data = PDict [
    (Tuple "nested" (PList [PInt 0, existing]))
]
