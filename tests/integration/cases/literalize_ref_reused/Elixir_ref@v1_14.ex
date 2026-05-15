defmodule Check do
  def x do
    shared_var = %{
        "_" => "_",
    }
    my_data = [
        shared_var,
        shared_var,
    ]
    _ = my_data
  end
end
