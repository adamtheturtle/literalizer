module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PList [PList [PDict [(Tuple "$ref" (PStr "myVar"))], PInt 42, PStr "static"]]
    ]
