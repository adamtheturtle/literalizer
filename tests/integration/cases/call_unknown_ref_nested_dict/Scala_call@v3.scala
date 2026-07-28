object Fixture_call_unknown_ref_nested_dict_Scala_call {
def process(data: Any = null): Any = null
val my_list = Map[String, String](
    "unused" -> "value",
)
process(data = List[List[Map[String, Map[String, String]]]](List[Map[String, Map[String, String]]](Map("inner" -> my_list))))
}
