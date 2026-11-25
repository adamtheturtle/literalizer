object Fixture_call_ref_args_trivial_register_Scala_heterogeneous_strategy_record_call {
def process(value: Any = null, count: Any = null): Any = null
val my_int = 1
val my_bool = true
val my_float = 3.14
val my_list = List[Int](
    1,
    2,
    3,
)
process(value = my_int, count = 42)
process(value = my_bool, count = 7)
process(value = my_float, count = 9)
process(value = my_list, count = 1)
}
