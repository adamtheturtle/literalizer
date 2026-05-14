module Check where


data Val
    = PSet (Array Val)


my_data :: Val
my_data = PSet []
