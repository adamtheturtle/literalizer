import java.math.BigInteger
data class Record0(val narrow_pair: Array<Any?>, val wide_pair: Array<Any?>, val wide_triple: Array<Any?>, val beyond_pair: Array<Any?>, val beyond_triple: Array<Any?>, val mixed_triple: Array<Any?>)
val my_data = Record0(
    narrow_pair = arrayOf<Any?>(
        1,
        2,
    ),
    wide_pair = arrayOf<Any?>(
        1L,
        1099511627776L,
    ),
    wide_triple = arrayOf<Any?>(
        1L,
        2L,
        1099511627776L,
    ),
    beyond_pair = arrayOf<Any?>(
        BigInteger("1"),
        BigInteger("18446744073709551616"),
    ),
    beyond_triple = arrayOf<Any?>(
        BigInteger("1"),
        BigInteger("2"),
        BigInteger("18446744073709551616"),
    ),
    mixed_triple = arrayOf<Any?>(
        1,
        "text",
        true,
    ),
)
