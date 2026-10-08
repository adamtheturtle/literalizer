module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "double" (PStr "a b")),
    (Tuple "single" (PStr "c d")),
    (Tuple "both" (PStr "e f g")),
    (Tuple "continued" (PStr "hi")),
    (Tuple "escaped backslash" (PStr "j\\ k"))
]
