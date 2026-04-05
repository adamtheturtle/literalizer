module Check where


data Val
    = PFloat Number
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PFloat 0.000000,
    PFloat 1.000000,
    PFloat 1500.000000,
    PFloat 0.001000
    ]
