module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PLong Number
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "a" (PInt 1)),
    (Tuple "b" (PLong 1099511627776.0))
    ]
