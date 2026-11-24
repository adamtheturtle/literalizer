module Check where


import Prelude
consume :: forall a0 a1 a2. a0 -> a1 -> a2 -> Unit
consume _ _ _ = unit


main :: Unit
main =
    let
        _ = consume ({ x: 1 }) (2) ("first")
        _ = consume ({ name: "Ada" }) (3) ("second")
    in
    unit
