object Fixture_literalize_ref_pre_indented_injected_text_Scala_ref {
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
