module Check where


data Tuple a b = Tuple a b
data Val
    = PFloat Number
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "pi" (PFloat 3.141592653589793))
    ]
