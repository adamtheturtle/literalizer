object Fixture_call_ref_args_reused_Scala_call {
def process(data: Any = null, count: Any = null): Any = null
val shared = 1
val other = 2
process(data = shared, count = 1)
process(data = other, count = 0)
process(data = shared, count = 8)
}
