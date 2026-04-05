module Check where


data Val
    = PStr String
    | PSet (Array Val)


my_data :: Val
my_data = PSet [
    -- before apple
    PStr "apple",
    PStr "banana"  -- banana inline
    -- trailing
    ]
