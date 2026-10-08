data class Record1(val value: Int)
data class Record0(val child: Record1)
val first = Record0(
    child = Record1(
        value = 1,
    ),
)
val my_data = first
