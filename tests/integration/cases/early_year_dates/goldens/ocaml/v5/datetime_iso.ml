module Check = struct

type val_t =
  | OStr of string
  | ODate of (int * int * int)
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("date", ODate (99, 5, 27));
    ("naive", OStr "0001-01-01T12:30:00");
    ("recent", OStr "2024-05-27T10:00:00")
]

end
