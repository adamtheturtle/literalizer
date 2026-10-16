val shared = intArrayOf(
    1,
    2,
)
var my_data = intArrayOf(
    0,
)
_ = &my_data;
my_data = shared
_ = &my_data;
