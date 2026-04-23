using System;
using System.IO;
using System.Linq;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;

var tpa = (string?)AppContext.GetData("TRUSTED_PLATFORM_ASSEMBLIES") ?? "";
var references = tpa.Split(Path.PathSeparator)
    .Where(f => !string.IsNullOrEmpty(f))
    .Select(f => (MetadataReference)MetadataReference.CreateFromFile(f))
    .ToList();

// Match the per-fixture .csproj that this host replaces:
// `<Nullable>disable</Nullable>` and `<ImplicitUsings>disable</ImplicitUsings>`
// — the fixtures bring their own `using` directives.
var options = new CSharpCompilationOptions(OutputKind.ConsoleApplication)
    .WithNullableContextOptions(NullableContextOptions.Disable);

var parseOptions = new CSharpParseOptions(LanguageVersion.Latest);

var input = Console.In.ReadToEnd();
var paths = input.Split('\0').Where(p => !string.IsNullOrEmpty(p)).ToList();

var allOk = true;
for (var i = 0; i < paths.Count; i++)
{
    var path = paths[i];
    var source = File.ReadAllText(path);
    var tree = CSharpSyntaxTree.ParseText(source, parseOptions, path: path);
    var compilation = CSharpCompilation.Create(
        assemblyName: $"fixture_{i}",
        syntaxTrees: new[] { tree },
        references: references,
        options: options);

    using var ms = new MemoryStream();
    var result = compilation.Emit(ms);
    if (!result.Success)
    {
        allOk = false;
        Console.Error.WriteLine($"{path}: C# compilation failed");
        foreach (var diag in result.Diagnostics.Where(d => d.Severity == DiagnosticSeverity.Error))
        {
            Console.Error.WriteLine($"  {diag}");
        }
    }
}

Environment.Exit(allOk ? 0 : 1);
