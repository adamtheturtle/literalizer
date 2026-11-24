module Check where


data Tuple a b = Tuple a b
data Val
    = PNull
    | PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PList [PDict [(Tuple "a" (PInt 1))], PDict [(Tuple "a" (PNull))], PInt 42],
    PList [PDict [(Tuple "a" (PInt 1))], PDict [(Tuple "a" (PStr "s"))], PInt 42],
    PList [PDict [(Tuple "a" (PInt 1))], PDict [(Tuple "a" (PNull))]],
    PList [PDict [(Tuple "a" (PInt 1))], PDict [(Tuple "a" (PStr "s"))]]
]
