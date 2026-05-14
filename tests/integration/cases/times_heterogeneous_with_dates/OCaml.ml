module Check = struct

type val_t =
  | OStr of string
  | ODate of (int * int * int)
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("vals", OList [ODate (2024, 1, 15); "09:30:00"])
]

end
