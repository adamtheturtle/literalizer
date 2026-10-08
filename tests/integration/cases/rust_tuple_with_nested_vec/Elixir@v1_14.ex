defmodule Check do
  def x do
    my_data = %{
        "lint" => [2, []],
        "test" => [5, ["compile"]],
        "package" => [7, ["link", "test"]],
    }
    _ = my_data
  end
end
