module Check where


data Tuple a b = Tuple a b
data Val
    = PNull
    | PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


actual :: Val
actual = PDict [
    (Tuple "_" (PStr "_"))
]
my_data :: Val
my_data = PList [
    PDict [(Tuple "$ref" (PInt 1))],
    PDict [(Tuple "$ref" (PNull))],
    actual
]
