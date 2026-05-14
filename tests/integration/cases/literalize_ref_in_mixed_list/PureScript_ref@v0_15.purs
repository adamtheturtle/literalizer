module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


refX :: Val
refX = PDict [
    (Tuple "_" (PStr "_"))
    ]
my_data :: Val
my_data = PList [
    refX,
    PInt 1,
    PInt 2
    ]
