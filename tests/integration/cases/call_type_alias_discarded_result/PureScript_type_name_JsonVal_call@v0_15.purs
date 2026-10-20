module Check where


import Prelude
data JsonVal
    = PInt Int
process :: JsonVal -> Unit
process _ = unit


main :: Unit
main =
    let
        _ = process (PInt 1)
    in
    unit
