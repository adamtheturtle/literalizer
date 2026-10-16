Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' null heading
        ' before null
        ' first null
        ' second null
        Dim my_data = New Dictionary(Of String, Object) From {
            {"a", Nothing},
            {"b", Nothing}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' null heading
        ' before null
        ' first null
        ' second null
        my_data = New Dictionary(Of String, Object) From {
            {"a", Nothing},
            {"b", Nothing}
        }
    End Sub
End Module
