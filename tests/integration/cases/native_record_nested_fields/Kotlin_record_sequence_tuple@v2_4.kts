data class Record1(val name: String, val active: Boolean)
data class Record2(val name: String, val score: Double)
data class Record0(val owner: Record1, val members: List<Record2>)
val my_data = Record0(
    owner = Record1(
        name = "Ada",
        active = false,
    ),
    members = listOf<Record2>(
        Record2(
            name = "Ada",
            score = 1.5,
        ),
        Record2(
            name = "Bob",
            score = 2.5,
        ),
    ),
)
