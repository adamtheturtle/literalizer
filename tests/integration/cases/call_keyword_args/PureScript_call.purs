module Check where


data Val
    = PFloat Number
    | PStr String
    | PList (Array Val)


print(throttler.check(PStr "user_1", PFloat 1000.0))
print(throttler.check(PStr "user_2", PFloat 2000.5))
