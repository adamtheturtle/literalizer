module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


stringMap :: Val
stringMap = PDict [
    (Tuple "k" (PStr "s"))
]
my_data :: Val
my_data = PList [
    stringMap,
    PDict [(Tuple "k" (PInt 1))]
]
