module Check where


data Val
    = PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    -- line 1
    -- line 2
    PStr "a"
    ]
