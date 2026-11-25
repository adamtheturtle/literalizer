data class Record1(val status: Int)
data class Record2(val status: String)
data class Record4(val kind: String, val urgent: Boolean)
data class Record3(val inner: Record4)
data class Record6(val error: String)
data class Record5(val inner: Record6)
data class Record7(val holder: Record1)
data class Record8(val holder: Record2)
data class Record9(val nums: List<Any?>)
data class Record0(val plain: Record1, val other: Record2, val nested_a: Record3, val nested_b: Record5, val wrap_a: Record7, val wrap_b: Record8, val wide: Record9)
val my_data = Record0(
    plain = Record1(
        status = 1,
    ),
    other = Record2(
        status = "ready",
    ),
    nested_a = Record3(
        inner = Record4(
            kind = "add",
            urgent = true,
        ),
    ),
    nested_b = Record5(
        inner = Record6(
            error = "not_found",
        ),
    ),
    wrap_a = Record7(
        holder = Record1(
            status = 2,
        ),
    ),
    wrap_b = Record8(
        holder = Record2(
            status = "word",
        ),
    ),
    wide = Record9(
        nums = listOf<Any?>(
            1L,
            1099511627776L,
        ),
    ),
)
