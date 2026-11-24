module Check where


import Prelude
import CallTarget as Target


main :: Unit
main =
    let
        _ = Target.consume (1)
    in
    unit
