module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "metrics" (PDict [(Tuple "count" (PInt 100)), (Tuple "rate" (PInt 50))])),
    (Tuple "flags" (PDict [(Tuple "retries" (PInt 3)), (Tuple "timeout" (PInt 30))]))
    ]
