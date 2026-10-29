module Check where


import Prelude
consume :: forall a0. a0 -> Unit
consume _ = unit


main :: Unit
main =
    let
        _ = consume ({ name: "Ada" })
    in
    unit
