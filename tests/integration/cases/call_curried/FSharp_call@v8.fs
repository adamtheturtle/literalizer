module Main

type Val =
    | FFloat of float
    | FStr of string
    | FList of Val list
type ThrottlerType_() =
    member _.check (_user_id: obj) (_ts: obj) : obj = null
let throttler = ThrottlerType_()
throttler.check (FStr "user_1") (FFloat 1000.0)
throttler.check (FStr "user_2") (FFloat 2000.5)
