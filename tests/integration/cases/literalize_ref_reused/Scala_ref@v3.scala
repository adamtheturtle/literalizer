object Fixture_literalize_ref_reused_Scala_ref {
val sharedVar = Map[String, String](
    "_" -> "_",
)
val my_data = List[Map[String, String]](
    sharedVar,
    sharedVar,
)
}
