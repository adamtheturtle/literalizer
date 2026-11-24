module Check where


import Prelude
app :: forall a0 a1. { client :: { consume :: a0 -> a1 -> Unit } }
app = { client: { consume: \_ _ -> unit } }


main :: Unit
main =
    let
        _ = app.client.consume ({ x: 1 }) (2)
        _ = app.client.consume ({ name: "Ada" }) (3)
    in
    unit
