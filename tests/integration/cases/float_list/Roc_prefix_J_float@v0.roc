module [my_data]

Val : [
    JFloat F64,
    JList (List Val),
]

my_data : Val
my_data = JList [
    JFloat 1.1,
    JFloat -2.2,
    JFloat 3.3,
    ]
