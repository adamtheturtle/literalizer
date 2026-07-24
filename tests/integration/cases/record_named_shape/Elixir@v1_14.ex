defmodule Check do
  def x do
    my_data = [
        %{"id" => 100, "label" => "first item", "enabled" => false, "related_ids" => [102, 103]},
        %{"id" => 101, "label" => "second item", "enabled" => true, "related_ids" => [100]},
    ]
    _ = my_data
  end
end
