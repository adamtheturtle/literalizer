module Check where


import Prelude
data Val
    = PInt Int


main :: Unit
main =
    let
        _ = PInt 42
    in
    unit
