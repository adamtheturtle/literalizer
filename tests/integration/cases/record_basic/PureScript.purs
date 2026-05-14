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
    (Tuple "id" (PInt 1)),
    (Tuple "description" (PStr "She said \"hello\", then waved")),
    (Tuple "is_done" (PBool false)),
    (Tuple "blocks" (PList [PInt 1, PInt 2, PInt 3]))
    ]
