object Fixture_call_ref_multiline_openers_Scala_call {
def consume(items: Any = null, mapping: Any = null): Any = null
val foo = 42
consume(items = List[Map[String, Int]](
    Map(
        "other" -> 1,
    ),
    foo,
), mapping = Map[String, Int](
    "left" -> foo,
    "other" -> 1,
))
}
