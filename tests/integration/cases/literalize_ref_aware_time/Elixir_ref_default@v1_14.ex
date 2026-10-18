defmodule Check do
  def x do
    shared_time = "12:30:15+02:00"
    my_data = %{
        "x" => shared_time,
    }
    _ = my_data
  end
end
