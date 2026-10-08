object Fixture_csharp_fallback_map_non_scalar_Scala_fallback_map_non_scalar {
case class Record0(name: String, payload: Map[String, Int])
val my_data = List(
    Record0(name = "one", payload = Map[String, Int]("scalar" -> 1, "items" -> List[Int](2, 3))),
    Record0(name = "two", payload = Map[String, Int]("other" -> 2)),
)
}
