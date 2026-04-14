module Check where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    a + b = error "not implemented"
    a * b = error "not implemented"
    abs a = error "not implemented"
    signum a = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HMap [
    ("level1", HMap [("level2", HMap [("level3", HMap [("level4", HMap [("value", HStr "deep"), ("items", HList [HStr "a", HStr "b"])])]), ("sibling", 42)]), ("tags", HList [HMap [("name", HStr "tag1"), ("meta", HMap [("priority", 1), ("labels", HList [HStr "x", HStr "y"])])]])])
    ]
