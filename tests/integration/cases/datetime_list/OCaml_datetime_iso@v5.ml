module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OStr "2024-01-15T12:30:00.123456+00:00";
    OStr "2024-06-01T08:00:00+00:00"
]

end
