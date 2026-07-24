data class NamedType(val id: Int, val label: String, val enabled: Boolean, val related_ids: IntArray)
data class Record0(val project: String, val lead_item: NamedType)
val my_data = Record0(
    project = "alpha",
    lead_item = NamedType(
        id = 100,
        label = "first item",
        enabled = false,
        related_ids = intArrayOf(
            102,
            103,
        ),
    ),
)
