module Check where

data Playlist = Playlist Val
data Val
    = PInt Int
    | PList (Array Val)
created = Playlist (PInt 1)
checked :: Boolean
checked = case created of
    Playlist (PInt 1) -> true
    _ -> false
