defmodule Check do
  def x do
    my_data = %{
        "a" => 0o1,
        "b" => 0o20000000000000,
    }
    _ = my_data
  end
end
