module Check = struct

module Api = struct
module Worker = struct
let process _ = ()
end
end
type val_t =
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let _ = Api.Worker.process(OMap [], OMap [])

end
