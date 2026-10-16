defmodule Check do
  def x do
    my_data = %{
        # outer heading
        # first empty
        "a" => %{},
        # second empty
        "b" => %{},
    }
    _ = my_data
  end
end
