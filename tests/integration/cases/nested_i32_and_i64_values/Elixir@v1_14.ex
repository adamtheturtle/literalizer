defmodule Check do
  def x do
    my_data = %{
        "values" => [1, 2147483648],
    }
    _ = my_data
  end
end
