module Check = struct

type val_t0 = { date : (int * int * int); naive : ((int * int * int) * (int * int * int)); recent : ((int * int * int) * (int * int * int)) }
let my_data = ({
    date = (99, 5, 27);
    naive = ((1, 1, 1), (12, 30, 0));
    recent = ((2024, 5, 27), (10, 0, 0))
} : val_t0)

end
