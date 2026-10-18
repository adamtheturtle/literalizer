module Check where


data Tuple a b = Tuple a b
data Val
    = PBool Boolean
    | PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "h" (PList [PInt 1, PStr "a", PList [PInt 2, PStr "b"], PDict [(Tuple "k" (PList [PBool true]))]]))
]
