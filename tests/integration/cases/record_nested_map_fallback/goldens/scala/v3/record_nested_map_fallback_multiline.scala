object Fixture_record_nested_map_fallback_Scala_record_nested_map_fallback_multiline {
case class Record0(name: String, input: Map[String, Any], expected: Map[String, Any])
val my_data = List(
    Record0(
        name = "test_1",
        input = Map[String, Any](
            "type" -> "create",
            "pr_id" -> "pr_1",
            "draft" -> true,
            "missing" -> null,
        ),
        expected = Map[String, Any](
            "pr_id" -> "pr_1",
            "status" -> "draft",
        ),
    ),
    Record0(
        name = "test_2",
        input = Map[String, Any](
            "type" -> "publish",
            "pr_id" -> "pr_1",
        ),
        expected = Map[String, Any](
            "error" -> "invalid_operation",
        ),
    ),
)
}
