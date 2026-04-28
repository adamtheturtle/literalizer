object Fixture_call_ref_args_Scala_call {
def process(data: Any = null, count: Any = null): Any = null
val my_var = List[Int](
    1,
    2,
    3,
)
val my_other = List[Int](
    4,
    5,
    6,
)
process(data = my_var, count = 42)
process(data = my_other, count = 7)
}
