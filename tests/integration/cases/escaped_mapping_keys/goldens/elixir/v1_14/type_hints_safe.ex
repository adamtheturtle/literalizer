defmodule Check do
  def x do
    my_data = %{
        "quote\"backslash\\" => 1,
        "line\nbreak" => 2,
        "$(literal)${text}" => 3,
        "RStr prefix" => 4,
    }
    _ = my_data
  end
end
