module Check where


data Tuple a b = Tuple a b
data Val
    = PBool Boolean
    | PInt Int
    | PFloat Number
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "d" (PList [PDict [(Tuple "a" (PList [PDict [(Tuple "b" (PList [PInt 1, PList [PFloat 2.5, PList [PStr "x", PList [PBool true]]]]))]]))]]))
]
