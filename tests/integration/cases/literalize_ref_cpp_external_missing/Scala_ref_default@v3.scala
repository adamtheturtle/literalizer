object Fixture_literalize_ref_cpp_external_missing_Scala_ref_default {
def consume_widget(_arg: Any = null): Any = null
val item = List[Int](
    1,
    2,
)
val my_data = List[Int](
    1,
    2,
)
consume_widget(_arg = my_data)
my_data = item
consume_widget(_arg = my_data)
}
