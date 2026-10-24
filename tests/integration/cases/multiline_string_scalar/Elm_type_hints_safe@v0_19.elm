module Check exposing (..)


type Val
    = EStr String


my_data : Val
my_data = EStr "\nroot first line\n  indented\n\nroot last line\n"
