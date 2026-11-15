module Check exposing (..)


type Val
    = Playlist
    | EBool Bool
    | EInt Int
    | EList (List Val)


my_data : Val
my_data = EList [
    Playlist,
    EBool True,
    EInt 1
    ]
