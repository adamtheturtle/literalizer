module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OStr "custom base after empty collision: )\"\nvalue";
    OStr "custom suffix after base collision: )\" and )x0\"\nvalue";
    OStr "custom second suffix: )\" and )x0\" and )x00\"\nvalue";
    OStr "long base exhaustion: )\" and )abcdefghijklmnop\"\nvalue"
]

end
