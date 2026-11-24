module Check = struct

type val_t =
  | JStr of string
  | JDate of (int * int * int)
  | JDatetime of ((int * int * int) * (int * int * int))
  | JMap of (string * val_t) list
let my_data : val_t = JMap [
    ("date", JDate (99, 5, 27));
    ("naive", JDatetime ((1, 1, 1), (12, 30, 0)));
    ("recent", JDatetime ((2024, 5, 27), (10, 0, 0)))
]

end
