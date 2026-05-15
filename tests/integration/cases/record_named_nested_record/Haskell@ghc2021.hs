module Fixture_record_named_nested_record_Haskell where
data Val = HBool Bool | HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
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
    ("project", HStr "alpha"),
    ("lead_task", HMap [("id", 100), ("description", HStr "first task"), ("is_done", HBool False), ("blocks", HList [102, 103])])
    ]
main :: IO ()
main = seq my_data (return ())
