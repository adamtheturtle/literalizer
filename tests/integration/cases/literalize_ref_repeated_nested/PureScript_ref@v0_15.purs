module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


shared :: Val
shared = PList [
    PInt 1,
    PInt 2
]
my_data :: Val
my_data = PList [
    PDict [(Tuple "left" (shared)), (Tuple "right" (shared))]
]
