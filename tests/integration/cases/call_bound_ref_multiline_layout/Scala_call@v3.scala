object Fixture_call_bound_ref_multiline_layout_Scala_call {
def f(value: Any = null): Any = null
val x = List[List[Int]](
    List[Int](
        1,
        2,
    ),
    List[Int](
        3,
        4,
    ),
)
f(value = List[List[List[List[Int]]]](
    List[List[List[Int]]](
        x,
    ),
))
}
