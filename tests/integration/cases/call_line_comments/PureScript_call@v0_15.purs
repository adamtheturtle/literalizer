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
        _ = process (PStr "Dune")  -- first edition
        _ = process (PStr "Solaris")
        _ = process (PStr "Neuromancer")  -- cyberpunk
    in
    unit
