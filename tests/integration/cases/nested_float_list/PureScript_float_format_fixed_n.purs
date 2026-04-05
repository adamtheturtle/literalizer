module Check where


data Val
    = PFloat Number
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PList [PFloat 1.500000, PFloat 2.500000],
    PList [PFloat 3.500000, PFloat 4.500000]
    ]
