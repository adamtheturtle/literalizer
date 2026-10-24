defmodule Check do
  def x do
    my_data = %{
        "a" => 1,
        "b" => 3_000_000_000,
        "c" => "x",
    }
    _ = my_data
  end
end
