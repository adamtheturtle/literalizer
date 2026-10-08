module Check where


data Tuple a b = Tuple a b
data Val
    = PNull
    | PBool Boolean
    | PInt Int
    | PFloat Number
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PDict [(Tuple "a" (PInt 1))],
    PInt 1,
    PStr "x",
    PBool true,
    PFloat 2.5,
    PNull
]
