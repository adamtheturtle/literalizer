object Fixture_call_ref_args_heterogeneous_list_Scala_heterogeneous_strategy_record_call {
def process(data: Any = null, count: Any = null): Any = null
val my_ints = List[Int](
    1,
    2,
    3,
)
val my_strings = List[String](
    "a",
    "b",
)
val my_empty = List()
process(data = my_ints, count = 42)
process(data = my_strings, count = 7)
process(data = my_empty, count = 99)
}
