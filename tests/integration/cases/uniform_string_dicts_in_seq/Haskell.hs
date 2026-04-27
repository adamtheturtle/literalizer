module check where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    HMap [("first", HStr "Alice"), ("last", HStr "Smith")],
    HMap [("first", HStr "Bob"), ("last", HStr "Jones")]
    ]
