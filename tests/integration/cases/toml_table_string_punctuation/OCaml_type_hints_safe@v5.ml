module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("comma_hash", OStr "a,#b");
    ("comma_space_hash", OStr "trail, # comment");
    ("escaped_quote", OStr "quote \" and , #");
    ("next_line", OStr "xy");
    ("line_separator", OStr "x y");
    ("paragraph_separator", OStr "x y")
]

end
