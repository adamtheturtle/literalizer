using System;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
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

// `LanguageVersion.CSharp10` matches `CSharp.language_version` in
// `src/literalizer/languages/csharp.py`; keep them in sync.
var parseOptions = new CSharpParseOptions(LanguageVersion.CSharp10);

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
        continue;
    }

    var assembly = Assembly.Load(ms.ToArray());
    try
    {
        // Top-level-statement fixtures compile to a synthetic
        // `<Program>$.<Main>$` whose body is the statement list, so
        // invoking the entry point runs their `var my_data = ...`
        // initializers.
        var entryPoint = assembly.EntryPoint;
        if (entryPoint is not null)
        {
            var parameters = entryPoint.GetParameters();
            object?[]? entryArgs = parameters.Length == 0
                ? null
                : new object?[] { Array.Empty<string>() };
            entryPoint.Invoke(obj: null, parameters: entryArgs);
        }
        // `class Check { ... Main() {} }` fixtures declare `my_data`
        // as a field whose initializer only runs when the class is
        // constructed; their `Main` is empty, so the entry point
        // alone never exercises the initializer. Force the static
        // cctor and — when there's a parameterless ctor — construct
        // an instance so instance field initializers run too.
        var checkType = assembly.GetType("Check");
        if (checkType is not null)
        {
            RuntimeHelpers.RunClassConstructor(checkType.TypeHandle);
            if (checkType.GetConstructor(Type.EmptyTypes) is not null)
            {
                Activator.CreateInstance(checkType);
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
        Console.Error.WriteLine($"{path}: C# runtime error: {inner}");
    }
}

Environment.Exit(allOk ? 0 : 1);
