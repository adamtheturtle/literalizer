module Check = struct

module Outer = struct
module Thing = struct
let go _ = ()
end
end
type val_t =
  | OList of val_t list
let _ = Outer.Thing.go()

end
