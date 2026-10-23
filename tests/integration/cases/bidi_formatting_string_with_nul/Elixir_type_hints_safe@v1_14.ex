defmodule Check do
  def x do
    my_data = %{
        "v" => "a\u202A\0é😀b",
    }
    _ = my_data
  end
end
