defmodule Check do
  def x do
    my_data = [
        %{"input" => %{"name" => "alice", "city" => "paris"}, "expected" => %{"count" => 1, "total" => 2}},
        %{"input" => %{"name" => 10, "city" => 20}, "expected" => %{"count" => "done", "total" => "pending"}},
    ]
    _ = my_data
  end
end
