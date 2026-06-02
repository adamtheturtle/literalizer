module Fixture_dict_colliding_cobol_keys_Haskell where
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
    ("user_name", 1),
    ("user.name", 2),
    ("user-name", 3),
    ("field_name_that_is_really_quite_long_one", 4),
    ("field_name_that_is_really_quite_long_two", 5)
    ]
main :: IO ()
main = seq my_data (return ())
