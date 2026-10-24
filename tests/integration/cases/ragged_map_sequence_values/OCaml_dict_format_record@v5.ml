module Check = struct

type val_t1 = { item : int list }
type val_t0 = { a : val_t1 list; b : val_t1 list }
let my_data = ({
    a = [
        ({
            item = [
                1
            ]
        } : val_t1)
    ];
    b = [
        ({
            item = [
                2;
                3
            ]
        } : val_t1)
    ]
} : val_t0)

end
