module [my_data]

Val : [
    RFloat F64,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RFloat 5.0e-324,
    RFloat 2.2250738585072014e-308,
    RFloat 1.0e-307,
    RFloat 1.0e21,
    RFloat -1.5e300,
    RFloat 1.7976931348623157e308,
    RFloat -1.7976931348623157e308,
]
