defmodule Check do
  def x do
    my_data = %{
        "a" => 1,
        "b" => "x",
        "e" => {1, 2},
        "f" => %{"g" => "h"},
    }
    _ = my_data
  end
end
