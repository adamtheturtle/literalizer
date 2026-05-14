defmodule MgrType_ do
  def run(_operation), do: nil
end
defmodule AppType_ do
  def mgr, do: MgrType_
end
defmodule Check do
  def x do
    app = AppType_
    app.mgr.run(%{"type" => "create", "pr_id" => "pr_1", "draft" => true})
    app.mgr.run(%{"type" => "create", "pr_id" => "pr_2"})
  end
end
