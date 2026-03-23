object Declaration {
  val my_data = Set[String](
      "apple",  // inline comment
      // before banana
      "banana",
      // trailing
  )
}
object Assignment {
  var my_data: Any = null
  my_data = Set[String](
      "apple",  // inline comment
      // before banana
      "banana",
      // trailing
  )
}
