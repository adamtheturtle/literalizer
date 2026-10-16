defmodule Check do
  def x do
    my_data = %{
        "astral" => "😀",
        "mixed" => "a😀b",
        "count" => 2,
        "list" => ["😀", 1],
        "nested" => %{"inner" => "😀"},
    }
    _ = my_data
  end
end
