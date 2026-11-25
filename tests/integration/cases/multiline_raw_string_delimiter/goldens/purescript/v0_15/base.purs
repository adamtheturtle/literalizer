module Check where


data Val
    = PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PStr "custom base after empty collision: )\"\nvalue",
    PStr "custom suffix after base collision: )\" and )x0\"\nvalue",
    PStr "custom second suffix: )\" and )x0\" and )x00\"\nvalue",
    PStr "long base exhaustion: )\" and )abcdefghijklmnop\"\nvalue"
]
