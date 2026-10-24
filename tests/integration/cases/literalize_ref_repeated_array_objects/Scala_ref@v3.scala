object Fixture_literalize_ref_repeated_array_objects_Scala_ref {
val shared = Array[Map[String, Int]](
    Map[String, Int]("value" -> 1),
)
val my_data = Array[Array[Map[String, Int]]](
    shared,
    shared,
)
}
