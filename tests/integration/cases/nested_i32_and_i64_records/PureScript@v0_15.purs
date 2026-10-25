module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PLong Number
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PList [PDict [(Tuple "value" (PInt 1))]],
    PList [PDict [(Tuple "value" (PLong 1099511627776.0))]]
]
