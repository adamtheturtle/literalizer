defmodule Check do
  def x do
    my_data = %{
        "a" => nil,
        "b" => nil,
        # trailing
    }
    _ = my_data
  end
end
