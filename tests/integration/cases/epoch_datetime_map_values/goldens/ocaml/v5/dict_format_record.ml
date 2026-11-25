module Check = struct

type val_t0 = { within_i32 : ((int * int * int) * (int * int * int)); beyond_i32 : ((int * int * int) * (int * int * int)) }
let my_data = ({
    within_i32 = ((2024, 1, 15), (12, 0, 0));
    beyond_i32 = ((2099, 6, 15), (8, 30, 0))
} : val_t0)

end
