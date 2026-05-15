object Fixture_call_ref_args_reused_Scala_heterogeneous_strategy_record_call {
def process(data: Any = null, count: Any = null): Any = null
val single_var = List[Int](
    4,
    5,
    6,
)
val repeated_var = 1
process(data = repeated_var, count = 1)
process(data = single_var, count = 0)
process(data = repeated_var, count = 8)
}
