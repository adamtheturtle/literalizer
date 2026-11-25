module Check = struct

type val_t =
  | OArray of val_t array
let process _ = ()
let untyped_value : val_t array = [||]
let _ = process([|untyped_value; untyped_value|])

end
