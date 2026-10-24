module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


-- empty heading
-- empty body
-- after empty
my_data :: Val
my_data = PDict []
