@file:Repository("file:///tmp/m2")
@file:DependsOn("org.jetbrains.kotlin:kotlin-compiler-embeddable:2.3.20")
@file:DependsOn("org.jetbrains.kotlin:kotlin-scripting-compiler-embeddable:2.3.20")

import org.jetbrains.kotlin.cli.common.ExitCode
import org.jetbrains.kotlin.cli.jvm.K2JVMCompiler
import kotlin.system.exitProcess

val files = System.`in`.bufferedReader().readText()
    .split('\u0000')
    .filter { it.isNotEmpty() }

val compiler = K2JVMCompiler()
var allOk = true

for (path in files) {
    val out = java.nio.file.Files.createTempDirectory("kotlin-lint-").toFile()
    try {
        val exit = compiler.exec(System.err, "-script", "-d", out.absolutePath, path)
        if (exit != ExitCode.OK) {
            System.err.println("Failed: $path")
            allOk = false
        }
    } finally {
        out.deleteRecursively()
    }
}

if (!allOk) exitProcess(1)
