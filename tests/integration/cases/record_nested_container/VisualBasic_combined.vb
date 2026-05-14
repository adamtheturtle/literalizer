Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"title", "report"},
            {"tags", New String() {"draft", "urgent", "review"}},
            {"priority", 2}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"title", "report"},
            {"tags", New String() {"draft", "urgent", "review"}},
            {"priority", 2}
        }
    End Sub
End Module
