module [my_data]

Val : [
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RStr "line1\r\nline2",
    RStr "line1\rline2",
    RStr "\u(0001)",
    ]
