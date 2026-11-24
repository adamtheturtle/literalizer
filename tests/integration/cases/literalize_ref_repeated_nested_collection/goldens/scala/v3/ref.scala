object Fixture_literalize_ref_repeated_nested_collection_Scala_ref {
val shared = List(
    List[Int](1, 2),
    Map[String, Int]("value" -> 1),
)
val my_data = List(
    shared,
    shared,
)
}
