module Check = struct

type val_t =
  | OStr of string
  | ODate of (int * int * int)
  | ODatetime of ((int * int * int) * (int * int * int))
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("date", ODate (99, 5, 27));
    ("naive", ODatetime ((1, 1, 1), (12, 30, 0)));
    ("recent", ODatetime ((2024, 5, 27), (10, 0, 0)))
]

end
