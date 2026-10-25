defmodule Check do
  def x do
            shared = [
                1,
                2,
            ]
            my_data = [
                # A leading comment with { braces, "quotes", and // markers
                "first\n{ \"quoted\" // text }",
                shared,
            ]
    _ = my_data
  end
end
