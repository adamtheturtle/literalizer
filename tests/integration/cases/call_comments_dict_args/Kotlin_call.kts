fun process(value: Any? = null): Any? = null
// Test cases
process(value = mapOf<String, String>("type" to "create", "pr_id" to "pr_1"))  // first case
process(value = mapOf<String, String>("type" to "update", "pr_id" to "pr_2"))  // second case
// third case
process(value = mapOf<String, String>("type" to "delete", "pr_id" to "pr_3"))
