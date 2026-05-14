module [my_data]

Val : [
    JStr Str,
    JList (List Val),
]

my_data : Val
my_data = JList [
    JStr "48656c6c6f",
    ]
