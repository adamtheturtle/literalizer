module Check = struct

type val_t0 = { exact_millisecond : string; sub_millisecond : string }
let my_data = ({
    exact_millisecond = "09:30:15.123000";
    sub_millisecond = "09:30:15.123456"
} : val_t0)

end
