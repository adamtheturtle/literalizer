using System;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
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

// `VisualBasic16_9` is the VB compiler version that ships with .NET 6
// and matches `Vb.language_version` in
// `src/literalizer/languages/vb.py`; keep them in sync.
var parseOptions = new VisualBasicParseOptions(LanguageVersion.VisualBasic16_9);

var input = Console.In.ReadToEnd();
var paths = input.Split('\0').Where(p => !string.IsNullOrEmpty(p)).ToList();

var allOk = true;
for (var i = 0; i < paths.Count; i++)
{
    var path = paths[i];
    var source = File.ReadAllText(path);
    var tree = VisualBasicSyntaxTree.ParseText(source, parseOptions, path: path);
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
        continue;
    }

    var assembly = Assembly.Load(ms.ToArray());
    var checkType = assembly.GetType("Check");
    if (checkType is null)
    {
        allOk = false;
        Console.Error.WriteLine($"{path}: expected `Module Check` but it was not found");
        continue;
    }
    try
    {
        // Module-level `Dim` initializers run in the type's cctor, so
        // forcing it exercises fixtures that define `my_data` directly
        // in `Module Check`.
        RuntimeHelpers.RunClassConstructor(checkType.TypeHandle);
        // Fixtures that wrap `my_data` inside `Sub _declaration()` and
        // `Sub _assignment()` only execute those bodies when the subs
        // are invoked, so call every declared parameterless shared sub.
        var methods = checkType.GetMethods(
            BindingFlags.Public | BindingFlags.Static | BindingFlags.DeclaredOnly);
        foreach (var method in methods)
        {
            if (method.GetParameters().Length == 0
                && method.ReturnType == typeof(void))
            {
                method.Invoke(obj: null, parameters: null);
            }
        }
    }
    catch (Exception ex)
    {
        allOk = false;
        // `RunClassConstructor` wraps cctor failures in
        // `TypeInitializationException`, and `MethodInfo.Invoke` wraps
        // callee failures in `TargetInvocationException`; peel both
        // layers so the reported error points at the fixture's actual
        // runtime failure.
        var inner = ex;
        while (inner is TargetInvocationException or TypeInitializationException
            && inner.InnerException is not null)
        {
            inner = inner.InnerException;
        }
        Console.Error.WriteLine($"{path}: VB runtime error: {inner}");
    }
}

Environment.Exit(allOk ? 0 : 1);
