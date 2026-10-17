module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PFloat Number
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "_" (PList [PInt 1, PFloat 2.5, PInt 3]))
]
