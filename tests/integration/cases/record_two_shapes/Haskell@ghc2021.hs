module Fixture_record_two_shapes_Haskell where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
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
    ("user", HMap [("id", 1), ("name", HStr "Alice")]),
    ("project", HMap [("title", HStr "report"), ("tags", HList [HStr "draft", HStr "urgent"])])
    ]
main :: IO ()
main = seq my_data (return ())
