module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_var :: Val
my_var = PInt 1
my_data :: Val
my_data = my_var
