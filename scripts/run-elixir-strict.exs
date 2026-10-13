# Evaluate the generated script with structured compiler diagnostics.
# Keep diagnostics visible and use their severity to determine failure.
{_, diagnostics} = Code.with_diagnostics([log: true], fn -> Code.eval_file(hd(System.argv())) end)
System.halt(if Enum.any?(diagnostics, &(&1.severity == :warning)), do: 1, else: 0)
