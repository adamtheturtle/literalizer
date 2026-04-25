using System;
var my_data = (
    (new DateOnly(2026, 1, 1), new DateOnly(2026, 1, 2)),
    ValueTuple.Create(),
    (new DateOnly(2026, 2, 3), new DateOnly(2026, 2, 4))
);
my_data = (
    (new DateOnly(2026, 1, 1), new DateOnly(2026, 1, 2)),
    ValueTuple.Create(),
    (new DateOnly(2026, 2, 3), new DateOnly(2026, 2, 4))
);
