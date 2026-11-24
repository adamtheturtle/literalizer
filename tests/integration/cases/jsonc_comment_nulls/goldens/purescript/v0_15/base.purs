module Check where


data Tuple a b = Tuple a b
data Val
    = PNull
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    -- null heading
    -- before null
    (Tuple "a" (PNull)),  -- first null
    (Tuple "b" (PNull))  -- second null
]
