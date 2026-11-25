module Check = struct

type val_t =
  | OStr of string
  | ODatetime of ((int * int * int) * (int * int * int))
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("within_i32", ODatetime ((2024, 1, 15), (12, 0, 0)));
    ("beyond_i32", ODatetime ((2099, 6, 15), (8, 30, 0)))
]

end
