module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OStr "中中中中中中中中中中中中中中中中中中中中";
    OStr "é'é'é'é'é'é'é'é'é'é'";
    OStr "🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂"
]

end
