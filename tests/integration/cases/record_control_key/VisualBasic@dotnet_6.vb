Imports System.Collections.Generic
Module Check
    Dim my_data = New Object() {
        New Dictionary(Of String, Object) From {{"a" & vbTab & "b" & Chr(10) & "c", 1}, {"id", "x"}}
    }
End Module
