module Check where


data Tuple a b = Tuple a b
data Val
    = PStr String
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "comma_hash" (PStr "a,#b")),
    (Tuple "comma_space_hash" (PStr "trail, # comment")),
    (Tuple "escaped_quote" (PStr "quote \" and , #")),
    (Tuple "next_line" (PStr "xy")),
    (Tuple "line_separator" (PStr "x y")),
    (Tuple "paragraph_separator" (PStr "x y"))
]
