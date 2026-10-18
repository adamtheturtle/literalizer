module Check = struct

type val_t0 = { positive : float; negative : float; nan_value : float; finite : float }
let my_data = ({
    positive = infinity;
    negative = neg_infinity;
    nan_value = nan;
    finite = 1.5
} : val_t0)

end
