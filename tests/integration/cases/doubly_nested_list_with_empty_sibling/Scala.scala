object Fixture_doubly_nested_list_with_empty_sibling_Scala {
val my_data = List[List[List[Int]]](
    List[List[Int]](List[Int](1, 2)),
    List[List[Int]](),
    List[List[Int]](List[Int](3, 4)),
)
}
