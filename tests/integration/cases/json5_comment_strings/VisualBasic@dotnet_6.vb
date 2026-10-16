Imports System.Collections.Generic
Module Check
    ' strings stay data
    ' URL annotation
    ' outside the string
    Dim my_data = New String() {
        "https://example.org/a/*b*/",
        "escaped quote: "" // still data",
        "backslash: \",
        "/* not a comment */"
    }
End Module
