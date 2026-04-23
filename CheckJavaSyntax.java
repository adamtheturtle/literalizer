import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import javax.tools.JavaCompiler;
import javax.tools.JavaFileObject;
import javax.tools.StandardJavaFileManager;
import javax.tools.ToolProvider;

// Compile each given Java source file with the in-process JavaCompiler
// API so the compiler stays warm across fixtures instead of cold-starting
// a JVM per file like the previous `javac` bash loop did.
public class CheckJavaSyntax {
    public static void main(final String[] args) throws IOException {
        final JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
        if (compiler == null) {
            System.err.println("No JDK Java compiler available.");
            System.exit(2);
        }
        boolean failed = false;
        try (final StandardJavaFileManager fileManager =
                compiler.getStandardFileManager(null, null, null)) {
            for (final String filename : args) {
                // Each fixture declares `class Check`, so give every file
                // its own output directory to avoid class-name collisions.
                final Path classDir = Files.createTempDirectory("javac");
                final Iterable<? extends JavaFileObject> units =
                        fileManager.getJavaFileObjectsFromStrings(List.of(filename));
                final JavaCompiler.CompilationTask task = compiler.getTask(
                        null,
                        fileManager,
                        null,
                        List.of("-d", classDir.toString(), "-proc:none"),
                        null,
                        units);
                if (!task.call()) {
                    System.err.println(filename + ": javac failed");
                    failed = true;
                }
            }
        }
        System.exit(failed ? 1 : 0);
    }
}
