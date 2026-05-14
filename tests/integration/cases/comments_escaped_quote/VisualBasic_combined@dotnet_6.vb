Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' real
        Dim my_data = New Dictionary(Of String, Object) From {
            {"key", "value "" # not a comment"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' real
        my_data = New Dictionary(Of String, Object) From {
            {"key", "value "" # not a comment"}
        }
    End Sub
End Module
