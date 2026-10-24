module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)


my_data : Val
my_data = EList (
    EList (EStr "\nfirst line\n  indented\n\nlast line\n" :: [])
     :: [])
