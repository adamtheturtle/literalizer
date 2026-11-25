data class Record1(val count: Int, val rate: Int)
data class Record2(val retries: Int, val timeout: Int)
data class Record0(val metrics: Record1, val flags: Record2)
val my_data = Record0(
    metrics = Record1(
        count = 100,
        rate = 50,
    ),
    flags = Record2(
        retries = 3,
        timeout = 30,
    ),
)
