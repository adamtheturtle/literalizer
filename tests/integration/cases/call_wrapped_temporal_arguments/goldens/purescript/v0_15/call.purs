module Check where


import Prelude
check :: Val -> Val -> Unit
check _ _ = unit
data Val
    = PStr String
    | PList (Array Val)


main :: Unit
main =
    let
        _ = check (PStr "2024-01-15T10:30:00+00:00") (PStr "2024-06-01")
    in
    unit
