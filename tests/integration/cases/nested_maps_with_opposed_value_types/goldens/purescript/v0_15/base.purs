module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PDict [(Tuple "input" (PDict [(Tuple "name" (PStr "alice")), (Tuple "city" (PStr "paris"))])), (Tuple "expected" (PDict [(Tuple "count" (PInt 1)), (Tuple "total" (PInt 2))]))],
    PDict [(Tuple "input" (PDict [(Tuple "name" (PInt 10)), (Tuple "city" (PInt 20))])), (Tuple "expected" (PDict [(Tuple "count" (PStr "done")), (Tuple "total" (PStr "pending"))]))]
]
