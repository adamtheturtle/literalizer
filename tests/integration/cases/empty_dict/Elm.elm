module Check exposing (..)


type Val
    = EDict (List ( String, Val ))


my_data : Val
my_data = EDict []
