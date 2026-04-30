module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PList [PList [PDict [(Tuple "$ref" (PStr "my_var"))], PInt 42, PStr "static"]],
    PList [PList [PDict [(Tuple "$ref" (PStr "my_other"))], PInt 7, PStr "label"]]
    ]
