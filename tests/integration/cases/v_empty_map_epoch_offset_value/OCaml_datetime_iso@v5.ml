module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OMap [("timestamp", OStr "2040-01-01T03:00:00+03:00")];
    OMap []
]

end
