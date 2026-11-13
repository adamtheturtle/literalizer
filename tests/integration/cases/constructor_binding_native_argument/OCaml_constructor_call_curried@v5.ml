module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
type playlist = Playlist of val_t
let created = Playlist (OInt 1)
let () = assert (created = Playlist (OInt 1))
end
