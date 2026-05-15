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
    PDict [(Tuple "id" (PInt 100)), (Tuple "description" (PStr "first task")), (Tuple "is_done" (PBool false)), (Tuple "blocks" (PList [PInt 102, PInt 103]))],
    PDict [(Tuple "id" (PInt 101)), (Tuple "description" (PStr "second task")), (Tuple "is_done" (PBool true)), (Tuple "blocks" (PList [PInt 100]))]
    ]
