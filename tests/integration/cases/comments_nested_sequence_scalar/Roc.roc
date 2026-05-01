module [my_data]

Val : [
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RList [RStr "ADD", RStr "alice", RStr "hello"],
    RList [RStr "DEL", RStr "bob", RStr "5"],  # removes "world"
    ]
