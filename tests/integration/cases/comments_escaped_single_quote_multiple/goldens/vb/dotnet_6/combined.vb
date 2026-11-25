Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' a comment
        ' another
        Dim my_data = New Dictionary(Of String, Object) From {
            {"host", "it's here"},
            {"port", 80}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' a comment
        ' another
        my_data = New Dictionary(Of String, Object) From {
            {"host", "it's here"},
            {"port", 80}
        }
    End Sub
End Module
