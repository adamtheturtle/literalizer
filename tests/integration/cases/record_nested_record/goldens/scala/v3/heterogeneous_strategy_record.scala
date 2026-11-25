object Fixture_record_nested_record_Scala_heterogeneous_strategy_record {
case class Record1(name: String, age: Int)
case class Record0(id: Int, owner: Record1)
val my_data = Record0(
    id = 1,
    owner = Record1(
        name = "Alice",
        age = 30,
    ),
)
}
