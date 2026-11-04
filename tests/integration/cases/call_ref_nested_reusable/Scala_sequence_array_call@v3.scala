object Fixture_call_ref_nested_reusable_Scala_sequence_array_call {
def process(data: Any = null): Any = null
val item = Array[Int](
    1,
    2,
)
process(data = Array[Array[Int]](item, item))
}
