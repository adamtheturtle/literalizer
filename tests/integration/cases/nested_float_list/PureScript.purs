module Check where


data Val
    = PFloat Number
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PList [PFloat 1.5, PFloat 2.5],
    PList [PFloat 3.5, PFloat 4.5]
    ]
