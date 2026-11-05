module Check = struct

type val_t1 = { value : int }
type val_t0 = { section : val_t1 }
let my_data = ({
    section = ({
        value = 1
    } : val_t1)
} : val_t0)

end
