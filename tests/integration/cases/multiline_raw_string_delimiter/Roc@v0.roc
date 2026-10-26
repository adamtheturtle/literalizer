module [my_data]

Val : [
    RStr Str,
    RList (List Val),
]

my_data : Val
my_data = RList [
    RStr "custom base after empty collision: )\"\nvalue",
    RStr "custom suffix after base collision: )\" and )x0\"\nvalue",
    RStr "custom second suffix: )\" and )x0\" and )x00\"\nvalue",
    RStr "long base exhaustion: )\" and )abcdefghijklmnop\"\nvalue",
]
