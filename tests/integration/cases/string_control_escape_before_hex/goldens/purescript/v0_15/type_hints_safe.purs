module Check where


data Val
    = PStr String


my_data :: Val
my_data = PStr "a\x07\x66\x61\x63\x65"
