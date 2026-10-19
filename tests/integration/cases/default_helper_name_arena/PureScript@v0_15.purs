module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


arena :: Val
arena = PDict [
    (Tuple "a" (PInt 1))
]
