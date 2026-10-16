Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' strings stay data
        ' URL annotation
        ' outside the string
        Dim my_data = New String() {
            "https://example.org/a/*b*/",
            "escaped quote: "" // still data",
            "backslash: \",
            "/* not a comment */"
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' strings stay data
        ' URL annotation
        ' outside the string
        my_data = New String() {
            "https://example.org/a/*b*/",
            "escaped quote: "" // still data",
            "backslash: \",
            "/* not a comment */"
        }
    End Sub
End Module
