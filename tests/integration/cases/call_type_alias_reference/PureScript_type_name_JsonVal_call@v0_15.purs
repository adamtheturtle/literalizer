module Check where


import Prelude
data JsonVal
    = PInt Int
process :: JsonVal -> Unit
process _ = unit
value :: JsonVal
value = PInt 1


main :: Unit
main =
    let
        _ = process value
    in
    unit
