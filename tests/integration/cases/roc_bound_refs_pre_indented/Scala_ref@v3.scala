object Fixture_roc_bound_refs_pre_indented_Scala_ref {
            val shared = List[Int](
                1,
                2,
            )
            val other = 3
            val payload = "\n    shared : Val\nshared = RInt 99"
            val my_data = Map(
                "a" -> shared,
                "b" -> other,
                "payload" -> payload,
            )
}
