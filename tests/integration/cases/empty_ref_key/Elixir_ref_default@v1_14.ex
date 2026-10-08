defmodule Check do
  def x do
    external_value = %{
        "_" => "_",
    }
    my_data = [
        external_value,
    ]
    _ = my_data
  end
end
