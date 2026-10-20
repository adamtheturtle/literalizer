module Check where


data Val
    = PInt Int
    | PList (Array Val)


refData :: Val
refData = PInt 1
my_data :: Val
my_data = refData
