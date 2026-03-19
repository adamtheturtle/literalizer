Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New HashSet(Of Object) From {
            "apple",  ' inline comment
            ' before banana
            "banana"
            ' trailing
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New HashSet(Of Object) From {
            "apple",  ' inline comment
            ' before banana
            "banana"
            ' trailing
        }
    End Sub
End Module
