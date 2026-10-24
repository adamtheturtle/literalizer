Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"outer", New String()() {New String() {"nested first line" & Chr(10) & "  indented" & Chr(10) & Chr(10) & "nested last line" & Chr(10)}}}
    }
End Module
