defmodule Check do
  def x do
    my_data = %{
        "lint" => [2, []],
        "test" => [5, ["compile"]],
    }
    _ = my_data
  end
end
