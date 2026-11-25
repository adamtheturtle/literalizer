defmodule Check do
  def x do
    my_data = %{
        "a" => 0b1,
        "b" => 0b10000000000000000000000000000000000000000,
    }
    _ = my_data
  end
end
