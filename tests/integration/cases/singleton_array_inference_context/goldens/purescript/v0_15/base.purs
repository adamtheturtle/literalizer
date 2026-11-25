module Check where


data Tuple a b = Tuple a b
data Val
    = PNull
    | PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "nil" (PList [PList [PList [PList [PList [PList [PList [PList [PList [PNull]]]]]]]]])),
    (Tuple "empty" (PList [PList [PList [PList [PList [PList [PList [PList [PList [PList []]]]]]]]]])),
    (Tuple "siblings" (PList [PList [PList [PList [PList [PList [PList [PList [PList [PList [PInt 4, PInt 5]]]]]]]]]]))
]
