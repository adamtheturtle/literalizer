object Fixture_literalize_ref_repeated_nested_Scala_ref {
val shared = List[Int](
    1,
    2,
)
val my_data = List[Map[String, List[Int]]](
    Map[String, List[Int]]("left" -> shared, "right" -> shared),
)
}
