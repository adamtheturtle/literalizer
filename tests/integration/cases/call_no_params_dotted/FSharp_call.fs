module Main

type Val =
    | FList of Val list
type ThrottlerType_() =
    member _.check() : obj = null
let throttler = ThrottlerType_()
throttler.check()
throttler.check()
