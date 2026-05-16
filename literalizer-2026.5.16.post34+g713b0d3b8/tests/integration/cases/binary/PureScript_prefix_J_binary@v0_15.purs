module Check where


data Val
    = JStr String
    | JList (Array Val)


my_data :: Val
my_data = JList [
    JStr "48656c6c6f"
    ]
