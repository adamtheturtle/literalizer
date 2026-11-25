module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


bound :: Val
bound = PInt 2
my_data :: Val
my_data = PDict [
    (Tuple "value" (bound))
]
