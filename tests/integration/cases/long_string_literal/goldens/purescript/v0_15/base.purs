module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "long_str" (PStr "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")),
    (Tuple "quoted" (PStr "a\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"b")),
    (Tuple "wide" (PStr "中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中"))
]
