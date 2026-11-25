defmodule Check do
  def x do
    my_data = [
        "C:\\path\\to\\file",
        "back\\\\slash",
        "hello \\\"world\\\"",
        "path\\to \"# file",
        "trailing\\",
        "both \"quotes''' here",
        "line1\\nline2\nwith newline",
    ]
    _ = my_data
  end
end
