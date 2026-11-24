module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("title", OStr "report");
    ("tags", OList [OStr "draft"; OStr "urgent"; OStr "review"]);
    ("priority", OInt 2)
]

end
