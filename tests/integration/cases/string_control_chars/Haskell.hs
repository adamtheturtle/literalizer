module Check where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "line1\r\nline2",
    HStr "line1\rline2",
    HStr "\x01"
    ]
