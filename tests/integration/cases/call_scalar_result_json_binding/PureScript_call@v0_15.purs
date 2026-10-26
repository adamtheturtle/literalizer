module Check where


import Prelude
make_widget :: Val -> Unit
make_widget _ = unit
data Val
    = PInt Int


my_data = make_widget (PInt 42)
