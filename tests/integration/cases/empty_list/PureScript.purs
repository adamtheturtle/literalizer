module Check where


data Val
    = PList (Array Val)


my_data :: Val
my_data = PList []
