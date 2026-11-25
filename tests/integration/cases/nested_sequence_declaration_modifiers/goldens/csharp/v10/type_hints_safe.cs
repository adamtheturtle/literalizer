using System;
var my_data = (
    ValueTuple.Create(),
    ValueTuple.Create(1),
    (1, 2),
    (1, "x", true, (object?)null),
    (1, 2, 3, 4, 5, 6, 7, 8)
);
    _ = my_data;
