module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "cr" (PStr "a\rb")),
    (Tuple "crlf" (PStr "a\r\nb")),
    (Tuple "lf" (PStr "a\nb"))
]
