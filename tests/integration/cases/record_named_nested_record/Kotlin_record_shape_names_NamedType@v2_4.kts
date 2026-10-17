data class NamedType(val id: Int, val label: String, val enabled: Boolean, val related_ids: IntArray)
data class Record0(val collection: String, val featured_entry: NamedType)
val my_data = Record0(
    collection = "alpha",
    featured_entry = NamedType(
        id = 100,
        label = "first entry",
        enabled = false,
        related_ids = intArrayOf(
            102,
            103,
        ),
    ),
)
