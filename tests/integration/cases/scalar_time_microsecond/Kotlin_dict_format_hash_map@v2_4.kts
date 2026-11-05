import java.time.LocalTime
val my_data = hashMapOf<String, LocalTime>(
    "exact_millisecond" to LocalTime.of(9, 30, 15, 123000000),
    "sub_millisecond" to LocalTime.of(9, 30, 15, 123456000),
)
