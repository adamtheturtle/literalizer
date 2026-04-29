module Check where


import Prelude
data Val
    = PStr String
    | PList (Array Val)
process :: Val -> Unit
process _ = unit


main :: Unit
main =
    let
        _ = -- Test cases
        _ = process (PStr "hello")  -- single word
        _ = process (PStr "hello world")  -- two words
        _ = -- trailing comment
    in
    unit
