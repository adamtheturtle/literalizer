module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "morning" ("09:30:00")),
    (Tuple "afternoon" ("14:15:00")),
    (Tuple "evening" ("23:59:59"))
    ]
