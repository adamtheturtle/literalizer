module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PDict [(Tuple "nested" (PDict [(Tuple "count" (PInt 1)), (Tuple "name" (PStr "value"))]))],
    PDict []
]
