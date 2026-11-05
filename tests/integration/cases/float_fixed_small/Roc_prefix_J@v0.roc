module [my_data]

Val : [
    JFloat F64,
    JList (List Val),
]

my_data : Val
my_data = JList [
    JFloat 1.0e-09,
    JFloat -1.0e-09,
]
