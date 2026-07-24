object Fixture_record_named_nested_record_Scala_record_shape_names_NamedType {
case class NamedType(id: Int, label: String, enabled: Boolean, related_ids: List[Int])
case class Record0(collection: String, featured_entry: NamedType)
val my_data = Record0(
    collection = "alpha",
    featured_entry = NamedType(
        id = 100,
        label = "first entry",
        enabled = false,
        related_ids = List[Int](
            102,
            103,
        ),
    ),
)
}
