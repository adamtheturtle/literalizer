data class Record0(val id: Int, val label: String, val enabled: Boolean, val related_ids: IntArray)
val my_data = Record0(
    id = 1,
    label = "She said \"hello\", then waved",
    enabled = false,
    related_ids = intArrayOf(
        1,
        2,
        3,
    ),
)
