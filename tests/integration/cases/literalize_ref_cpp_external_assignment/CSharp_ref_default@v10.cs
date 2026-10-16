using System;
var ref_data = (
    1,
    2
);
var my_data = ValueTuple.Create(
    0
);
(void)my_data;
my_data = ref_data;
(void)my_data;
