data class Record1(val name: String, val age: Int)
data class Record0(val id: Int, val owner: Record1)
val my_data = Record0(
    id = 1,
    owner = Record1(
        name = "Alice",
        age = 30,
    ),
)
