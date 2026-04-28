import java.io.IOException;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.URL;
import java.net.URLClassLoader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import javax.tools.JavaCompiler;
import javax.tools.JavaFileObject;
import javax.tools.StandardJavaFileManager;
import javax.tools.ToolProvider;

// Compile and execute each given Java source file with the in-process
// JavaCompiler API and a private URLClassLoader so the compiler and JVM
// stay warm across fixtures instead of cold-starting a JVM per file like
// the previous `javac` bash loop did. Fixtures either expose a
// `public static void main()` method (wrapping the literal in a method
// body) or declare `my_data` as a field on `class Main`; either way the
// host triggers static-init, constructs a `Main` instance to run any
// instance-field initializers, and invokes `main()` when present, so
// runtime errors (e.g. a bad `Instant.parse` argument) surface here
// instead of passing silently.
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
                // Each fixture declares `class Main`, so give every file
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
                    continue;
                }
                if (!runFixture(filename, classDir)) {
                    failed = true;
                }
            }
        }
        System.exit(failed ? 1 : 0);
    }

    // Load `Main` from a private class loader rooted at *classDir*,
    // construct an instance (forcing both static- and instance-field
    // initializers), and invoke `main()` if the fixture defines one.
    // `Main` is package-private in every fixture, so `setAccessible`
    // is required before invoking members reflectively.
    private static boolean runFixture(final String filename, final Path classDir) {
        final URL[] urls;
        try {
            urls = new URL[] {classDir.toUri().toURL()};
        } catch (final java.net.MalformedURLException e) {
            System.err.println(filename + ": " + e);
            return false;
        }
        try (final URLClassLoader loader = new URLClassLoader(urls)) {
            final Class<?> checkClass = Class.forName("Main", true, loader);
            final Constructor<?> constructor = checkClass.getDeclaredConstructor();
            constructor.setAccessible(true);
            final Object instance = constructor.newInstance();
            final Method checkMethod;
            try {
                checkMethod = checkClass.getDeclaredMethod("main");
            } catch (final NoSuchMethodException e) {
                // Field-only fixtures — constructing `Main` above
                // already ran the field initializer.
                return true;
            }
            checkMethod.setAccessible(true);
            checkMethod.invoke(instance);
            return true;
        } catch (final InvocationTargetException e) {
            System.err.println(filename + ": " + e.getCause());
            return false;
        } catch (final Throwable t) {
            // Includes `ExceptionInInitializerError` (extends `Error`)
            // raised when a static field initializer throws during
            // `Class.forName`, e.g. a bad `Instant.parse` argument.
            System.err.println(filename + ": " + t);
            return false;
        }
    }
}
