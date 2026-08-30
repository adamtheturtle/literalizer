module Check where


import Prelude
data Val
    = PStr String
    | PList (Array Val)
f :: Val -> Unit
f _ = unit


main :: Unit
main =
    let
        _ = f (PList [PList [PStr "DEL", PStr "b", PStr "10"], PList [PStr "ADD", PStr "a", PStr "x"]])  -- note
    in
    unit
