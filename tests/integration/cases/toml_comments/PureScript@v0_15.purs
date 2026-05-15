module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    -- before
    (Tuple "answer" (PInt 42)),  -- inline
    (Tuple "plain" (PStr "ok"))
    -- trailing
    ]
