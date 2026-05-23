@file:DependsOn("org.jetbrains.kotlin:kotlin-compiler-embeddable:2.3.20")
@file:DependsOn("org.jetbrains.kotlin:kotlin-scripting-compiler-embeddable:2.3.20")

import org.jetbrains.kotlin.cli.common.ExitCode
import org.jetbrains.kotlin.cli.jvm.K2JVMCompiler
import kotlin.system.exitProcess

val files = System.`in`.bufferedReader().readText()
    .split('\u0000')
    .filter { it.isNotEmpty() }

// Optional `LITERALIZER_LINT_CLASSPATH` (colon-separated, with `dir/*`
// wildcards expanded to every jar in `dir/`) is forwarded to the
// per-script compiler so json_type fixtures resolve against
// kotlinx-serialization-json at lint time.  See `Lint Kotlin` in
// `.github/workflows/lint.yml` for the wiring.
val extraClasspath = (System.getenv("LITERALIZER_LINT_CLASSPATH") ?: "")
    .split(":")
    .filter { it.isNotEmpty() }
    .flatMap { entry ->
        if (entry.endsWith("/*")) {
            val dir = java.nio.file.Paths.get(entry.dropLast(2))
            java.nio.file.Files.newDirectoryStream(dir, "*.jar").use { stream ->
                stream.map { it.toString() }.sorted()
            }
        } else {
            listOf(entry)
        }
    }
val classpathArgs = if (extraClasspath.isEmpty()) {
    emptyList()
} else {
    listOf("-classpath", extraClasspath.joinToString(separator = ":"))
}

val compiler = K2JVMCompiler()
var allOk = true

for (path in files) {
    val out = java.nio.file.Files.createTempDirectory("kotlin-lint-").toFile()
    try {
        // `-language-version 1.9` and `-api-version 1.9` match
        // `Kotlin.language_version` in `src/literalizer/languages/kotlin.py`;
        // keep them in sync.
        val args = mutableListOf(
            "-script",
            "-language-version", "1.9",
            "-api-version", "1.9",
            "-d", out.absolutePath,
        )
        args.addAll(classpathArgs)
        args.add(path)
        val exit = compiler.exec(System.err, *args.toTypedArray())
        if (exit != ExitCode.OK) {
            System.err.println("Failed: $path")
            allOk = false
        }
    } finally {
        out.deleteRecursively()
    }
}

if (!allOk) exitProcess(1)
