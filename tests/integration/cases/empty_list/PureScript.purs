module Check where


import Prelude
data Val
    = PList (Array Val)


my_data :: Val
my_data = PList []
