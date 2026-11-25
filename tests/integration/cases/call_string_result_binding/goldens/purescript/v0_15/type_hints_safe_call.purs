module Check where


import Prelude
make_widget :: Val -> Unit
make_widget _ = unit
data Val
    = PStr String


my_data = make_widget (PStr "text")
