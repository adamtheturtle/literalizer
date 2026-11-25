Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' before
        ' inline
        ' trailing
        Dim my_data = New Dictionary(Of String, Object) From {
            {"answer", 42},
            {"plain", "ok"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' before
        ' inline
        ' trailing
        my_data = New Dictionary(Of String, Object) From {
            {"answer", 42},
            {"plain", "ok"}
        }
    End Sub
End Module
