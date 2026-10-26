defmodule Check do
  def x do
    my_data = %{
        "a" => 0o777777777777777777777,
        "b" => 0o1000000000000000000000,
    }
    _ = my_data
  end
end
