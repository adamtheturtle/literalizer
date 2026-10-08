module Check exposing (..)


type Val
    = EFloat Float
    | EList (List Val)


my_data : Val
my_data = EList [
    EFloat 5.0e-324,
    EFloat 2.2250738585072014e-308,
    EFloat 1.0e-307,
    EFloat 1.0e21,
    EFloat (-1.5e300),
    EFloat 1.7976931348623157e308,
    EFloat (-1.7976931348623157e308)
    ]
