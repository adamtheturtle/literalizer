import java.math.BigInteger
data class Record0(val quantity: Int, val big: BigInteger, val ratio: Double, val label: String, val ok: Boolean)
val my_data = Record0(
    quantity = 0b11110100001001000000,
    big = BigInteger("18446744073709551615"),
    ratio = 2.5,
    label = "tag",
    ok = true,
)
