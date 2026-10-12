@file:DependsOn("org.jetbrains.kotlin:kotlin-compiler-embeddable:2.3.20")
@file:DependsOn("org.jetbrains.kotlin:kotlin-scripting-compiler-embeddable:2.3.20")

import org.jetbrains.kotlin.cli.common.ExitCode
import org.jetbrains.kotlin.cli.jvm.K2JVMCompiler
import java.util.Locale
import java.util.Timer
import java.util.TimerTask
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
val timeoutSeconds = System.getenv("LITERALIZER_KOTLIN_TIMEOUT_SECONDS")?.toLong() ?: 60L
require(timeoutSeconds in 1L..1800L) {
    "LITERALIZER_KOTLIN_TIMEOUT_SECONDS must be between 1 and 1800"
}

for (path in files) {
    val out = java.nio.file.Files.createTempDirectory("kotlin-lint-").toFile()
    // A compiler/evaluation stall must not consume the entire lint job.
    // Synchronize cancellation so a completed fixture's timer cannot
    // terminate the JVM while the next fixture is being checked.
    val guardLock = Any()
    var completed = false
    val started = System.nanoTime()
    val cleanup = Thread { out.deleteRecursively() }
    Runtime.getRuntime().addShutdownHook(cleanup)
    val deadline = Timer("kotlin-fixture-deadline", true)
    deadline.schedule(object : TimerTask() {
        override fun run() {
            synchronized(guardLock) {
                if (!completed) {
                    val elapsed = (System.nanoTime() - started) / 1_000_000_000.0
                    val elapsedText = String.format(Locale.ROOT, "%.2f", elapsed)
                    System.err.println(
                        "$path: compiler/evaluation deadline (${timeoutSeconds}s) " +
                            "exceeded after ${elapsedText}s"
                    )
                    exitProcess(124)
                }
            }
        }
    }, timeoutSeconds * 1000L)
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
        synchronized(guardLock) {
            completed = true
            deadline.cancel()
        }
        Runtime.getRuntime().removeShutdownHook(cleanup)
        out.deleteRecursively()
    }
}

if (!allOk) exitProcess(1)
