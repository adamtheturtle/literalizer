module Check

type Val =
    | FFloat of float
    | FStr of string
    | FList of Val list
type _throttlerType() =
    member _.check (a: obj, b: obj) : obj = a
let throttler = _throttlerType()
let print (a: obj) : obj = a
print(throttler.check("user_1"; 1000.0))
print(throttler.check("user_2"; 2000.5))
