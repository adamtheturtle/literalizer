defmodule Check do
  def x do
    my_data = %{
        # null heading
        # before null
        "a" => nil,  # first null
        "b" => nil,  # second null
    }
    _ = my_data
  end
end
