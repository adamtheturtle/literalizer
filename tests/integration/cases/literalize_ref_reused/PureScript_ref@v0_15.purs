module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


sharedVar :: Val
sharedVar = PDict [
    (Tuple "_" (PStr "_"))
    ]
my_data :: Val
my_data = PList [
    sharedVar,
    sharedVar
    ]
