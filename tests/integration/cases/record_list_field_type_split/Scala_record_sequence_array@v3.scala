object Fixture_record_list_field_type_split_Scala_record_sequence_array {
case class Record1(kind: String, urgent: Boolean)
case class Record0(entries: Array[Any])
case class Record2(error: String)
val my_data = scala.collection.immutable.ListMap(
    "left" -> Record0(entries = Array(Record1(kind = "add", urgent = true))),
    "right" -> Record0(entries = Array(Record2(error = "not_found"))),
)
}
