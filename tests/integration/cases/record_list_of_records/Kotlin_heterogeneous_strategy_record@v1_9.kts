data class Record1(val id: Int, val label: String)
data class Record0(val name: String, val items: List<Any?>)
val my_data = Record0(
    name = "box",
    items = listOf<Any?>(
        Record1(
            id = 1,
            label = "first",
        ),
        Record1(
            id = 2,
            label = "second",
        ),
    ),
)
