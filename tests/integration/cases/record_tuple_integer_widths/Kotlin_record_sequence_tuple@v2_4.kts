import java.math.BigInteger
data class Record0(val narrow_pair: Pair<Int, Int>, val wide_pair: Pair<Long, Long>, val wide_triple: Triple<Long, Long, Long>, val beyond_pair: Pair<BigInteger, BigInteger>, val beyond_triple: Triple<BigInteger, BigInteger, BigInteger>, val mixed_triple: Triple<Int, String, Boolean>)
val my_data = Record0(
    narrow_pair = Pair(
        1,
        2,
    ),
    wide_pair = Pair(
        1L,
        1099511627776L,
    ),
    wide_triple = Triple(
        1L,
        2L,
        1099511627776L,
    ),
    beyond_pair = Pair(
        BigInteger("1"),
        BigInteger("18446744073709551616"),
    ),
    beyond_triple = Triple(
        BigInteger("1"),
        BigInteger("2"),
        BigInteger("18446744073709551616"),
    ),
    mixed_triple = Triple(
        1,
        "text",
        true,
    ),
)
