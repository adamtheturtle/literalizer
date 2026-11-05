object Fixture_record_root_nested_map_annotations_Scala_record_sequence_seq {
case class Record0(x: Int)
val my_data = scala.collection.immutable.ListMap(
    "outer" -> Seq(scala.collection.immutable.ListMap("inner" -> Record0(x = 1)), scala.collection.immutable.ListMap("inner" -> Record0(x = 2))),
)
}
