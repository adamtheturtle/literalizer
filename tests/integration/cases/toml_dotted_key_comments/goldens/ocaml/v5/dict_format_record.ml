module Check = struct

type val_t1 = { b : int; c : int }
type val_t0 = { a : val_t1 }
let my_data = ({
    a = ({
        b = 1;
        c = 2
    } : val_t1)
} : val_t0)

end
