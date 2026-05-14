defmodule Check do
  def x do
    my_data = %{
        "user" => %{"id" => 1, "name" => "Alice"},
        "project" => %{"title" => "report", "tags" => ["draft", "urgent"]},
    }
    _ = my_data
  end
end
