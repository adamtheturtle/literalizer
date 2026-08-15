data class Record1(val x: String)
data class Record2(val x: Int)
data class Record0(val direct: Record1, val bound: Record2)
val first = Record2(
    x = 1,
)
val my_data = Record0(
    direct = Record1(
        x = "s",
    ),
    bound = first,
)
