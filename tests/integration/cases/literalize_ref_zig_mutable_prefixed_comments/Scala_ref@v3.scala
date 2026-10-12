object Fixture_literalize_ref_zig_mutable_prefixed_comments_Scala_ref {
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
