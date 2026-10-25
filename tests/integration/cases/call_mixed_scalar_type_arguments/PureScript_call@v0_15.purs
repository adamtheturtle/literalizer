module Check where


import Prelude
data Val
    = PFloat Number
    | PStr String
    | PList (Array Val)
capture :: Val -> Val -> Val -> Val -> Val -> Val -> Val -> Unit
capture _ _ _ _ _ _ _ = unit


main :: Unit
main =
    let
        _ = capture (PFloat (0.0 / 0.0)) (PFloat (1.0 / 0.0)) (PFloat (-(1.0 / 0.0))) (PFloat 1.25) (PStr "2024-01-15") (PStr "2024-01-15T12:34:56") (PStr "[ordinary text]")
    in
    unit
