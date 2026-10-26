module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
module Api = struct
let process _ = ()
end
let _ = Api.process(OMap [])

end
