object Fixture_dict_colliding_normalized_long_keys_Scala_combined {
var my_data = Map[String, Int](
    "a_b" -> 1,
    "a-b" -> 2,
    "averyveryverylongkeynamethatgoesonandonandon" -> 3,
    "averyveryverylongkeynamethatgoesonandmore" -> 4,
)
my_data = Map[String, Int](
    "a_b" -> 1,
    "a-b" -> 2,
    "averyveryverylongkeynamethatgoesonandonandon" -> 3,
    "averyveryverylongkeynamethatgoesonandmore" -> 4,
)
}
