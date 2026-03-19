Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"key" & Chr(10) & "with" & Chr(10) & "newlines", "value1"},
        {"key" & vbTab & "with" & vbTab & "tabs", "value2"},
        {"", "value3"}
    }
End Module
