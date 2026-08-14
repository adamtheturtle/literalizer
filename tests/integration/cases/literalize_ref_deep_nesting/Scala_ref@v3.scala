object Fixture_literalize_ref_deep_nesting_Scala_ref {
val deep = List[List[String]](
    List[String](
        "one",
        "two",
    ),
    List[String](
        "three",
        "four",
    ),
)
val my_data = Map(
    "a" -> Map(
        "b" -> Map[String, List[List[String]]](
            "c" -> deep,
        ),
    ),
)
}
