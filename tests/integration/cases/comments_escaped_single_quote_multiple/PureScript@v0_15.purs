module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "host" (PStr "it's here")),  -- a comment
    (Tuple "port" (PInt 80))  -- another
    ]
