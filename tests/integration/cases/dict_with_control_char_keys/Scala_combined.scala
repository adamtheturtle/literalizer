object check {
var my_data = Map[String, String](
    "key\nwith\nnewlines" -> "value1",
    "key\twith\ttabs" -> "value2",
    "" -> "value3",
)
my_data = Map[String, String](
    "key\nwith\nnewlines" -> "value1",
    "key\twith\ttabs" -> "value2",
    "" -> "value3",
)
}
