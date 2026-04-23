def paths = System.in.text.split('\0').findAll { it }
def failed = false
paths.each { p ->
    try {
        new GroovyShell().parse(new File(p)).run()
    } catch (Throwable t) {
        System.err.println("FAIL ${p}:\n${t.message}")
        failed = true
    }
}
System.exit(failed ? 1 : 0)
