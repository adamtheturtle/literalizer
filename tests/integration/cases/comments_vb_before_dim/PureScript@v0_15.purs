module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    -- Configuration
    (Tuple "name" (PStr "app")),
    -- Port setting
    (Tuple "port" (PInt 3000))
    ]
