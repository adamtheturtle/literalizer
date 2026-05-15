module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "items" (PList [PDict [(Tuple "id" (PInt 1))], PDict [(Tuple "id" (PInt 2)), (Tuple "count" (PInt 10))], PDict [(Tuple "id" (PInt 3)), (Tuple "count" (PInt 20))]]))
    ]
