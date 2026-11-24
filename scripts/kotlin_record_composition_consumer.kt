fun consume(first: Record0, second: Record0, again: Record0) {
    check(first.name == "first")
    check(first.values.contentEquals(intArrayOf(1, 2)))
    check(second.name == "second")
    check(second.values.contentEquals(intArrayOf(3, 4)))
    check(second === again)
    println("""{"matched":true}""")
}
