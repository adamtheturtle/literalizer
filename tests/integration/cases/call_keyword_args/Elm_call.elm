module Check exposing (..)


type Val
    = EFloat Float
    | EStr String
    | EList (List Val)


print(throttler.check(EStr "user_1", EFloat 1000.0))
print(throttler.check(EStr "user_2", EFloat 2000.5))
