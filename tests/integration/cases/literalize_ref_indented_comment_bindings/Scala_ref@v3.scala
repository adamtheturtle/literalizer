object Fixture_literalize_ref_indented_comment_bindings_Scala_ref {
        val shared = List[Int](
            1,
            2,
        )
        val my_data = List(
            // A leading comment with { braces, "quotes", and // markers
            "first\n{ \"quoted\" // text }",
            shared,
        )
}
