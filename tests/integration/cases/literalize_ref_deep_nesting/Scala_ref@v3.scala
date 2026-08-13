object Fixture_literalize_ref_deep_nesting_Scala_ref {
val deep = List[List[Int]](
    List[Int](
        1,
        2,
    ),
    List[Int](
        3,
        4,
    ),
)
val my_data = Map(
    "a" -> Map(
        "b" -> Map(
            "c" -> deep,
        ),
    ),
)
}
