data class Record1(val id: Int, val label: String)
data class Record0(val name: String, val items: List<Record1>)
val my_data = Record0(
    name = "box",
    items = listOf<Record1>(
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
