module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    -- event time
    (Tuple "when" (PStr "2024-01-15T12:34:56+00:00"))
]
