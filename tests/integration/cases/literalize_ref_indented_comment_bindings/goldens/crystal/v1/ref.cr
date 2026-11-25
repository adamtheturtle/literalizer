module Fixture_literalize_ref_indented_comment_bindings_Crystal_ref
extend self
        shared = [
            1,
            2,
        ]
        my_data = [
            # A leading comment with { braces, "quotes", and // markers
            "first\n{ \"quoted\" // text }",
            shared,
        ]
end
