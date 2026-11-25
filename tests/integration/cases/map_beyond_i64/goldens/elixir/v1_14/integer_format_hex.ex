defmodule Check do
  def x do
    my_data = %{
        "a" => 0x7fffffffffffffff,
        "b" => 0x8000000000000000,
    }
    _ = my_data
  end
end
