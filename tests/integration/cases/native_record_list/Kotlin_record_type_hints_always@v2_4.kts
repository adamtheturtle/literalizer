data class Record1(val age: Int)
data class Record0(val name: String, val active: Boolean, val count: Int, val score: Double, val missing: Any?, val scores: IntArray, val child: Record1)
val my_data: List<Record0> = listOf<Record0>(
    Record0(name = "Ada", active = true, count = 1, score = 1.5, missing = null, scores = intArrayOf(1, 2), child = Record1(age = 3)),
    Record0(name = "Bob", active = false, count = 2, score = 2.5, missing = null, scores = intArrayOf(4), child = Record1(age = 5)),
)
