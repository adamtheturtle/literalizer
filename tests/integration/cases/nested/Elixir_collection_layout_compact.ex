defmodule Check do
  def x do
    my_data = %{
        "users" => [%{"name" => "Bob", "tags" => ["admin", "user"]}, %{"name" => "Carol", "tags" => ["guest"]}],
    }
    _ = my_data
  end
end
