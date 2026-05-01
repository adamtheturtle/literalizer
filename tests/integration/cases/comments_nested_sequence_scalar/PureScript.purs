module Check where


data Val
    = PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PList [PStr "ADD", PStr "alice", PStr "hello"],
    PList [PStr "DEL", PStr "bob", PStr "5"]  -- removes "world"
    ]
