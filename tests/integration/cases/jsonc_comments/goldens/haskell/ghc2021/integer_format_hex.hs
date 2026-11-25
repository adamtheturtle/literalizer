module Fixture_jsonc_comments_Haskell_integer_format_hex where
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
    -- A JSONC input case with both comment forms.
    ("url", HStr "https://example.org/a/*b*/"),  -- detail
    -- continued
    ("count", 0x2)  -- trailing line comment
    ]
main :: IO ()
main = seq my_data (return ())
