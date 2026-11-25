datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SStr "custom base after empty collision: )\"\nvalue",
    SStr "custom suffix after base collision: )\" and )x0\"\nvalue",
    SStr "custom second suffix: )\" and )x0\" and )x00\"\nvalue",
    SStr "long base exhaustion: )\" and )abcdefghijklmnop\"\nvalue"
]
val _ = my_data
