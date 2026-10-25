module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


std : Val
std = EDict [
    ("a", EInt 1)
    ]
arena : Val
arena = EDict [
    ("a", EInt 1)
    ]
allocator : Val
allocator = EDict [
    ("a", EInt 1)
    ]
my_data : Val
my_data = EList [
    std,
    arena,
    allocator
    ]
