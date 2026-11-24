module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OMap [("timestamp", OStr "2020-01-01T00:00:00+00:00")];
    OMap []
]

end
