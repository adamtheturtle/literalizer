module Main

type Val =
    | FFloat of float
    | FStr of string
    | FList of Val list
type ThrottlerType_() =
    member _.check(_user_id: obj, _ts: obj) : obj = null
let throttler = ThrottlerType_()
let emit (__arg: obj) : obj = null
emit(throttler.check("user_1", 1000.0))
emit(throttler.check("user_2", 2000.5))
