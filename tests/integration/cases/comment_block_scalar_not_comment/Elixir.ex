defmodule Check do
  def x do
    my_data = %{
        "description" => "# not a comment\n",
        "name" => "foo",
    }
    _ = my_data
  end
end
