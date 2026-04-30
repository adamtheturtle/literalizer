module Check where


import Prelude
data Val
    = PList (Array Val)
process :: Unit
process = unit
emit :: forall a. a -> Unit
emit _ = unit


main :: Unit
main =
    let
        _ = emit(process)
        _ = emit(process)
    in
    unit
