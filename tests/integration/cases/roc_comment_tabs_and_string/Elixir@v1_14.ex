defmodule Check do
  def x do
    my_data = %{
        # before	line
        "value" => "left\tright",  # inline	line
        # after	line
    }
    _ = my_data
  end
end
