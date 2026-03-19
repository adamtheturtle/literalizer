Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New HashSet(Of Object) From {
            "apple",
            "banana",
            "cherry"
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New HashSet(Of Object) From {
            "apple",
            "banana",
            "cherry"
        }
    End Sub
End Module
