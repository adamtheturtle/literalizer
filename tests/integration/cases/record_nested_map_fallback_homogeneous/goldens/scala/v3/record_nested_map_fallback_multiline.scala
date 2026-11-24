object Fixture_record_nested_map_fallback_homogeneous_Scala_record_nested_map_fallback_multiline {
case class Record1(kind: String, pr_id: String)
case class Record0(name: String, input: Record1, expected: Map[String, String])
val my_data = List(
    Record0(
        name = "test_1",
        input = Record1(
            kind = "create",
            pr_id = "pr_1",
        ),
        expected = Map[String, String](
            "pr_id" -> "pr_1",
            "status" -> "draft",
        ),
    ),
    Record0(
        name = "test_2",
        input = Record1(
            kind = "publish",
            pr_id = "pr_1",
        ),
        expected = Map[String, String](
            "error" -> "invalid_operation",
        ),
    ),
)
}
