module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    -- before	line
    (Tuple "value" (PStr "left\tright"))  -- inline	line
    -- after	line
]
