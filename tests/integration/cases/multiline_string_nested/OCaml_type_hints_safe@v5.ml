module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("outer", OList [OList [OStr "nested first line\n  indented\n\nnested last line\n"]])
]

end
