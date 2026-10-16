defmodule Check do
  def x do
    my_data = [
        # strings stay data
        "https://example.org/a/*b*/",  # URL annotation
        "escaped quote: \" // still data",
        "backslash: \\",  # outside the string
        "/* not a comment */",
    ]
    _ = my_data
  end
end
