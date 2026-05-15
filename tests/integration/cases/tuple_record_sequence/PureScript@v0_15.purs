module Check where


data Tuple a b = Tuple a b
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PList [
    PDict [(Tuple "call" (PStr "send")), (Tuple "args" (PList [PInt 1, PStr "email", PStr "a@gmail.com", PInt 100]))],
    PDict [(Tuple "call" (PStr "recv")), (Tuple "args" (PList [PInt 2, PStr "sms", PStr "b@example.com", PInt 200]))]
    ]
