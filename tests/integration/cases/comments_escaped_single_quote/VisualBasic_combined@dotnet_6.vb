Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' a comment
        Dim my_data = New Dictionary(Of String, Object) From {
            {"key", "it's here"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' a comment
        my_data = New Dictionary(Of String, Object) From {
            {"key", "it's here"}
        }
    End Sub
End Module
