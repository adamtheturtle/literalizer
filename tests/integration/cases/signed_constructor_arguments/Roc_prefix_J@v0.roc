module [my_data]

Val : [
    JInt I128,
    JFloat F64,
    JList (List Val),
]

my_data : Val
my_data = JList [
    JInt -42i128,
    JInt 0i128,
    JInt 42i128,
    JFloat -1.25,
    JFloat 0.0,
    JFloat 1.25,
]
