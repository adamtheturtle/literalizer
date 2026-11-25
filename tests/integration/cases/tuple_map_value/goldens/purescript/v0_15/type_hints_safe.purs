module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "rows" (PList [PDict [(Tuple "x" (PInt 1)), (Tuple "y" (PStr "a"))], PDict [(Tuple "x" (PInt 2)), (Tuple "y" (PStr "b"))]]))
]
