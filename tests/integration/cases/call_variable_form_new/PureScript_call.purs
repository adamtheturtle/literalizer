module Check where


make_widget :: Val -> Unit
make_widget _ = unit
data Val
    = PInt Int


result :: Val
result = make_widget (PInt 42)
