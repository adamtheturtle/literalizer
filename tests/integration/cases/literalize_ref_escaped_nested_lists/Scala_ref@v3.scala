object Fixture_literalize_ref_escaped_nested_lists_Scala_ref {
val existing = 1
val my_data = List(
    0,
    List[List[Int]](List[Int](existing)),
)
}
