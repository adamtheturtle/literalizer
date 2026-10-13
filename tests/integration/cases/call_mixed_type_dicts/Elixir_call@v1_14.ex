defmodule MgrType_ do
  def run(_operation), do: nil
end
defmodule Check do
  def x do
    app = %{mgr: MgrType_}
    app.mgr.run(%{"type" => "create", "pr_id" => "pr_1", "draft" => true})
    app.mgr.run(%{"type" => "create", "pr_id" => "pr_2"})
  end
end
