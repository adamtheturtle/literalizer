data class Record1(val a: Int, val b: String, val c: Any?)
data class Record0(val outer: Record1)
val my_data = Record0(
    outer = Record1(
        a = 1,
        b = "x",
        c = null,
    ),
)
