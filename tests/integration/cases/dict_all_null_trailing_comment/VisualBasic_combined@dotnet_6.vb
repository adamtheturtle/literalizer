Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' trailing
        Dim my_data = New Dictionary(Of String, Object) From {
            {"a", Nothing},
            {"b", Nothing}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' trailing
        my_data = New Dictionary(Of String, Object) From {
            {"a", Nothing},
            {"b", Nothing}
        }
    End Sub
End Module
