object Fixture_csharp_epoch_nested_array_width_Scala_sequence_array_epoch {
val my_data = Map(
    "positive" -> Array[Map[String, Array[Long]]](Map[String, Array[Long]]("item" -> Array[Long](2147483648L))),
    "negative" -> Array[Map[String, Array[Long]]](Map[String, Array[Long]]("item" -> Array[Long](-2147483649L))),
    "mixed" -> Array[Map[String, Array[Long]]](Map[String, Array[Long]]("item" -> Array[Long](0L, 2147483648L))),
)
}
