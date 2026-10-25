module Main

type Val =
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FStr "custom base after empty collision: )\"\nvalue";
    FStr "custom suffix after base collision: )\" and )x0\"\nvalue";
    FStr "custom second suffix: )\" and )x0\" and )x00\"\nvalue";
    FStr "long base exhaustion: )\" and )abcdefghijklmnop\"\nvalue"
]
