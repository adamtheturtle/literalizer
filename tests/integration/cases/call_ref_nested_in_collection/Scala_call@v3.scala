object Fixture_call_ref_nested_in_collection_Scala_call {
def process(a: Any = null, b: Any = null): Any = null
val big_list = List[String](
    "x",
)
process(a = Map[String, List[String]]("k" -> big_list), b = 2)
}
