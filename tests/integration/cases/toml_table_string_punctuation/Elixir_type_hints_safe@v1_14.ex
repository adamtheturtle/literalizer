defmodule Check do
  def x do
    my_data = %{
        "comma_hash" => "a,#b",
        "comma_space_hash" => "trail, # comment",
        "escaped_quote" => "quote \" and , #",
        "next_line" => "x\u0085y",
        "line_separator" => "x\u2028y",
        "paragraph_separator" => "x\u2029y",
    }
    _ = my_data
  end
end
