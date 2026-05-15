module Check where


data Tuple a b = Tuple a b
data Val
    = PBool Boolean
    | PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "project" (PStr "alpha")),
    (Tuple "lead_task" (PDict [(Tuple "id" (PInt 100)), (Tuple "description" (PStr "first task")), (Tuple "is_done" (PBool false)), (Tuple "blocks" (PList [PInt 102, PInt 103]))]))
    ]
