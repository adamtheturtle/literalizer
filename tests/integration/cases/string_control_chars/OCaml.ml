module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OStr "line1\r\nline2";
    OStr "line1\rline2";
    OStr ""
]

end
