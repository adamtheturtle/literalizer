module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OStr "C:\\path\\to\\file";
    OStr "back\\\\slash";
    OStr "hello \\\"world\\\"";
    OStr "path\\to \"# file";
    OStr "trailing\\";
    OStr "both \"quotes''' here";
    OStr "line1\\nline2\nwith newline"
]

end
