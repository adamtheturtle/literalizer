def paths = System.in.text.split('\0').findAll { it }
def failed = false
paths.each { p ->
    try {
        def file = new File(p)
        new GroovyShell().parse(file.text, file.name).run()
    } catch (Throwable t) {
        System.err.println("FAIL ${p}:\n${t.message}")
        failed = true
    }
}
System.exit(failed ? 1 : 0)
