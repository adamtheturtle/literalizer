def paths = System.in.text.split('\0').findAll { it }
def failed = false
paths.each { p ->
    try {
        // Groovy derives a class name from the script filename which
        // rejects ``@`` in identifiers; strip the ``@<version>`` tag
        // every fixture filename carries before parsing.
        def file = new File(p)
        def stem = file.name.replaceFirst(/\.groovy$/, '')
        def sanitized = stem.replaceFirst(/@.*$/, '') + '.groovy'
        new GroovyShell().parse(file.text, sanitized).run()
    } catch (Throwable t) {
        System.err.println("FAIL ${p}:\n${t.message}")
        failed = true
    }
}
System.exit(failed ? 1 : 0)
