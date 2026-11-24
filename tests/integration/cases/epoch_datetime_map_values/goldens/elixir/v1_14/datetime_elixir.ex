defmodule Check do
  def x do
    my_data = %{
        "within_i32" => ~N[2024-01-15 12:00:00],
        "beyond_i32" => ~N[2099-06-15 08:30:00],
    }
    _ = my_data
  end
end
