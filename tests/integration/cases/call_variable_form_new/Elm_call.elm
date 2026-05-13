module Check exposing (..)


make_widget : a -> ()
make_widget _ = ()
type Val
    = EInt Int


result : Val
result = make_widget (EInt 42)
