module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    -- first dotted key
    -- second dotted key
    (Tuple "a" (PDict [(Tuple "b" (PInt 1)), (Tuple "c" (PInt 2))]))
]
