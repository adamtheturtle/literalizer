using System;
using System.IO;
using System.Linq;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.VisualBasic;

var tpa = (string?)AppContext.GetData("TRUSTED_PLATFORM_ASSEMBLIES") ?? "";
var references = tpa.Split(Path.PathSeparator)
    .Where(f => !string.IsNullOrEmpty(f))
    .Select(f => (MetadataReference)MetadataReference.CreateFromFile(f))
    .ToList();

// Match the Microsoft.NET.Sdk VB defaults — these imports are set
// implicitly by `dotnet build` on a bare VB project, so the fixtures
// rely on them even when they don't say so.
var globalImports = GlobalImport.Parse(
    "Microsoft.VisualBasic",
    "System",
    "System.Collections",
    "System.Collections.Generic",
    "System.Data",
    "System.Diagnostics",
    "System.Linq",
    "System.Xml.Linq",
    "System.Threading.Tasks"
).ToList();

var options = new VisualBasicCompilationOptions(OutputKind.DynamicallyLinkedLibrary)
    .WithGlobalImports(globalImports)
    .WithOptionInfer(true)
    .WithOptionExplicit(true)
    .WithOptionStrict(OptionStrict.Off);

var input = Console.In.ReadToEnd();
var paths = input.Split('\0').Where(p => !string.IsNullOrEmpty(p)).ToList();

var allOk = true;
for (var i = 0; i < paths.Count; i++)
{
    var path = paths[i];
    var source = File.ReadAllText(path);
    var tree = VisualBasicSyntaxTree.ParseText(source, path: path);
    var compilation = VisualBasicCompilation.Create(
        assemblyName: $"fixture_{i}",
        syntaxTrees: new[] { tree },
        references: references,
        options: options);

    using var ms = new MemoryStream();
    var result = compilation.Emit(ms);
    if (!result.Success)
    {
        allOk = false;
        Console.Error.WriteLine($"{path}: VB compilation failed");
        foreach (var diag in result.Diagnostics.Where(d => d.Severity == DiagnosticSeverity.Error))
        {
            Console.Error.WriteLine($"  {diag}");
        }
    }
}

Environment.Exit(allOk ? 0 : 1);
