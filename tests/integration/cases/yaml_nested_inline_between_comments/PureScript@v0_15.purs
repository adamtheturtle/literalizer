module Check where


data Val
    = PInt Int
    | PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PList [PInt 2, PStr "hello"],  -- trailing note
    -- next element
    PList [PInt 3, PStr "world"]
    ]
