object Declaration {
  val my_data = List[Array[Array[Int]]](
      List[Array[Int]](List[Int](1, 2), List[Int](3, 4)),
      List[Array[Int]](List[Int](5)),
  )
}
object Assignment {
  var my_data: Any = null
  my_data = List[Array[Array[Int]]](
      List[Array[Int]](List[Int](1, 2), List[Int](3, 4)),
      List[Array[Int]](List[Int](5)),
  )
}
