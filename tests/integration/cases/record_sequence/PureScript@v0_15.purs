module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PDict [(Tuple "id" (PInt 1)), (Tuple "label" (PStr "first"))],
    PDict [(Tuple "id" (PInt 2)), (Tuple "label" (PStr "second"))],
    PDict [(Tuple "id" (PInt 3)), (Tuple "label" (PStr "third"))]
    ]
