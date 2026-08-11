object Fixture_dict_colliding_normalized_long_keys_Scala {
val my_data = Map[String, Int](
    "a_b" -> 1,
    "a-b" -> 2,
    "averyveryverylongkeynamethatgoesonandonandon" -> 3,
    "averyveryverylongkeynamethatgoesonandmore" -> 4,
)
}
