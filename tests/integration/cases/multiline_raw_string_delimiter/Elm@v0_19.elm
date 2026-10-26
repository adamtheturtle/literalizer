module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EStr "custom base after empty collision: )\"\nvalue",
    EStr "custom suffix after base collision: )\" and )x0\"\nvalue",
    EStr "custom second suffix: )\" and )x0\" and )x00\"\nvalue",
    EStr "long base exhaustion: )\" and )abcdefghijklmnop\"\nvalue"
    ]
