Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"quote""backslash\", 1},
            {"line" & Chr(10) & "break", 2},
            {"$(literal)${text}", 3},
            {"RStr prefix", 4}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"quote""backslash\", 1},
            {"line" & Chr(10) & "break", 2},
            {"$(literal)${text}", 3},
            {"RStr prefix", 4}
        }
    End Sub
End Module
