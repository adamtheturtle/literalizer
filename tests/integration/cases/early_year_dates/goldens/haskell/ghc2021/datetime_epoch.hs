module Fixture_early_year_dates_Haskell_datetime_epoch where
import Data.Time (Day, fromGregorian)
data Val = HStr String | HMap [(String, Val)] | HDate Day | HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HMap [
    ("date", HDate (fromGregorian 99 5 27)),
    ("naive", -62135551800),
    ("recent", 1716804000)
    ]
main :: IO ()
main = seq my_data (return ())
