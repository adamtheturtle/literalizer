module Check = struct

type val_t =
  | OStr of string
  | ODatetime of ((int * int * int) * (int * int * int))
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("date", OStr "0099-05-27");
    ("naive", ODatetime ((1, 1, 1), (12, 30, 0)));
    ("recent", ODatetime ((2024, 5, 27), (10, 0, 0)))
]

end
