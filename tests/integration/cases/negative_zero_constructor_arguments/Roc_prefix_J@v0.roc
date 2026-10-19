module [my_data]

Val : [
    JFloat F64,
    JList (List Val),
]

my_data : Val
my_data = JList [
    JFloat -0.0,
    JFloat 0.0,
]
