defmodule Check do
  def x do
    my_data = %{
        "a" => 1,  # inline ending backslash \ .
        "b" => 2,
    }
    _ = my_data
  end
end
