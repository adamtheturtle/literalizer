data class Record1(val a: Int)
data class Record0(val items: List<Record1>)
val my_data = Record0(
    items = listOf<Record1>(
        Record1(
            a = 1,
        ),
    ),
)
