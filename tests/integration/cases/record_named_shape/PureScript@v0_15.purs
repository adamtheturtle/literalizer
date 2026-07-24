module Check where


data Tuple a b = Tuple a b
data Val
    = PBool Boolean
    | PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PDict [(Tuple "id" (PInt 100)), (Tuple "label" (PStr "first item")), (Tuple "enabled" (PBool false)), (Tuple "related_ids" (PList [PInt 102, PInt 103]))],
    PDict [(Tuple "id" (PInt 101)), (Tuple "label" (PStr "second item")), (Tuple "enabled" (PBool true)), (Tuple "related_ids" (PList [PInt 100]))]
    ]
