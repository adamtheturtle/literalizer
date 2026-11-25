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
    (Tuple "values" (PList [PInt 1, PLong 2147483648.0]))
]
