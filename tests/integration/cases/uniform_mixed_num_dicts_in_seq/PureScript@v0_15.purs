module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PFloat Number
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PDict [(Tuple "x" (PInt 1)), (Tuple "y" (PFloat 2.5))],
    PDict [(Tuple "x" (PInt 3)), (Tuple "y" (PFloat 4.0))]
    ]
