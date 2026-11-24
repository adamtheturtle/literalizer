module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PLong Number
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "a" (PList [PInt 1])),
    (Tuple "b" (PList [PLong 1099511627776.0]))
]
