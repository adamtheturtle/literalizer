module Check where


data Val
    = PInt Int
    | PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PStr "This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.",
    PInt 1
    ]
