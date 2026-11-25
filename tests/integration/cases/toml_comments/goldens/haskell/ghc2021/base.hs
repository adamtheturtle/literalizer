module Fixture_toml_comments_Haskell where
data Val = HInt Integer | HStr String | HMap [(String, Val)]
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
    -- before
    ("answer", 42),  -- inline
    ("plain", HStr "ok")
    -- trailing
    ]
main :: IO ()
main = seq my_data (return ())
