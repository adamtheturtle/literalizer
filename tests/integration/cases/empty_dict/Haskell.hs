module Check where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap []
