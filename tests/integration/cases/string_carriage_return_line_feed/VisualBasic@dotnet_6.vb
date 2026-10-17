Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"cr", "a" & Chr(13) & "b"},
        {"crlf", "a" & vbCrLf & "b"},
        {"lf", "a" & Chr(10) & "b"}
    }
End Module
