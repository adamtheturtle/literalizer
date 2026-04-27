module Check where


data Val
    = PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PStr "line1\r\nline2",
    PStr "line1\rline2",
    PStr "\x01"
    ]
