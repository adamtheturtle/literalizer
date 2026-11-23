module Check exposing (..)


type Val
    = EList (List Val)


my_data : Val
my_data = EList []
