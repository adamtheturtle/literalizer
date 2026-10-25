object Fixture_literalize_ref_indented_comment_bindings_Scala_declaration_style_var_ref {
        var shared = List[Int](
            1,
            2,
        )
        var my_data = List(
            // A leading comment with { braces, "quotes", and // markers
            "first\n{ \"quoted\" // text }",
            shared,
        )
}
