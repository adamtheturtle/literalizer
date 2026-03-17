object Declaration {
  val my_data = Map(
      // Server configuration
      "host" -> "localhost",  // default host
      "port" -> 8080,
      // Enable debug mode
      "debug" -> true,
  )
}
object Assignment {
  var my_data: Any = null
  my_data = Map(
      // Server configuration
      "host" -> "localhost",  // default host
      "port" -> 8080,
      // Enable debug mode
      "debug" -> true,
  )
}
