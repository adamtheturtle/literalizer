defmodule Check do
  def x do
    my_data = %{
        "a" => 0x1,
        "b" => 0x10000000000,
    }
    _ = my_data
  end
end
