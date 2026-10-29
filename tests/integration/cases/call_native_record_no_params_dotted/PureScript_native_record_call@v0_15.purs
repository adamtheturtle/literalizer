module Check where


import Prelude
app :: { client :: { consume :: Unit } }
app = { client: { consume: unit } }


main :: Unit
main =
    let
        _ = app.client.consume
    in
    unit
