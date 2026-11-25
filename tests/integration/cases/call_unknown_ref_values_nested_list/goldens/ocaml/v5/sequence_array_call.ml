module Check = struct

type val_t =
  | OArray of val_t array
let process _ = ()
let unknown_value : val_t array = [||]
let _ = process([|unknown_value|])

end
