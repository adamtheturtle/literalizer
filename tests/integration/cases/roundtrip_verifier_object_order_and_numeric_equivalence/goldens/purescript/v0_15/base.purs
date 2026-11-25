module Check where


data Tuple a b = Tuple a b
data Val
    = PNull
    | PBool Boolean
    | PFloat Number
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "b" (PNull)),
    (Tuple "a" (PDict [(Tuple "y" (PList [PFloat 1.0])), (Tuple "x" (PBool false))]))
]
