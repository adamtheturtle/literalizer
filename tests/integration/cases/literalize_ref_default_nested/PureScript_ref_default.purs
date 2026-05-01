module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


item_var :: Val
item_var = PDict [
    (Tuple "_" (PStr "_"))
    ]
my_data :: Val
my_data = PDict [
    (Tuple "items" (PList [item_var, PDict [(Tuple "fallback" (PStr "value"))]]))
    ]
