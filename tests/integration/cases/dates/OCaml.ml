module Check = struct

type val_t =
  | OStr of string
  | ODate of (int * int * int)
  | ODatetime of ((int * int * int) * (int * int * int))
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("date", ODate (2024, 1, 15));
    ("datetime", ODatetime ((2024, 1, 15), (12, 30, 0)))
]

end
