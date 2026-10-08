module Check where


import Prelude
data Val
    = PFloat Number
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PFloat 5.0e-324,
    PFloat 2.2250738585072014e-308,
    PFloat 1.0e-307,
    PFloat 1.0e21,
    PFloat (-1.5e300),
    PFloat 1.7976931348623157e308,
    PFloat (-1.7976931348623157e308)
]
