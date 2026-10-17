val my_data = listOf<Map<String, Map<String, Map<String, Int>>>>(
    mapOf<String, Map<String, Map<String, Int>>>("outer" to mapOf<String, Map<String, Int>>("inner" to mapOf<String, Int>("x" to 1))),
    mapOf<String, Map<String, Map<String, Int>>>("outer" to mapOf<String, Map<String, Int>>("inner" to mapOf<String, Int>())),
)
