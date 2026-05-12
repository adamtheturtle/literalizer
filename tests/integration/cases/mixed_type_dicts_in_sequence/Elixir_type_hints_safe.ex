defmodule Check do
  def x do
    my_data = [
        %{"type" => "create", "pr_id" => "pr_1", "draft" => true},
        %{"type" => "create", "pr_id" => "pr_2"},
    ]
    _ = my_data
  end
end
