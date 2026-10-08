module Check = struct

type val_t0 = { positive : float; negative : float; nan_value : float }
let my_data = ({
    positive = infinity;
    negative = neg_infinity;
    nan_value = nan
} : val_t0)

end
