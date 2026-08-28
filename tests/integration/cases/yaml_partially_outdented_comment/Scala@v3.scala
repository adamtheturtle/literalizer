object Fixture_yaml_partially_outdented_comment_Scala {
val my_data = Map(
    "a" -> Map(
        "b" -> List[Int](1),
        // Outdented from the sequence, so the inner mapping claims this.
        "c" -> 2,
    ),
    // Outdented from the inner mapping too, so the root claims this.
    "d" -> 3,
)
}
