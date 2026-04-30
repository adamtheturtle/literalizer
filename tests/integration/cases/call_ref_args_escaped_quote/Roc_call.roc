module [main]

Val : [
    RStr Str,
    RList (List Val),
]
process : a -> {}
process = \_ -> {}

my_str : Val
my_str = RStr "a\"b"
main =
    dbg (process my_str)
    {}
