defmodule Check do
  def x do
    my_data = %{
        "a" => 9223372036854775807,
        "b" => 9223372036854775808,
    }
    _ = my_data
  end
end
