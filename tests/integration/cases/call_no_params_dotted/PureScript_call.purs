module Check where


import Prelude
data Val
    = PList (Array Val)
throttler :: { check :: Unit }
throttler = { check: unit }


main :: Unit
main =
    let
        _ = throttler.check
        _ = throttler.check
    in
    unit
