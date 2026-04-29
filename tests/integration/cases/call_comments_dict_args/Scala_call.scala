object Fixture_call_comments_dict_args_Scala_call {
def process(value: Any = null): Any = null
// Test cases
process(value = Map[String, String]("type" -> "create", "pr_id" -> "pr_1"))  // first case
process(value = Map[String, String]("type" -> "update", "pr_id" -> "pr_2"))  // second case
// third case
process(value = Map[String, String]("type" -> "delete", "pr_id" -> "pr_3"))
}
