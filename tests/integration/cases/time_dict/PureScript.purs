module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "morning" (PStr "09:30:00")),
    (Tuple "afternoon" (PStr "14:15:00")),
    (Tuple "evening" (PStr "23:59:59"))
    ]
