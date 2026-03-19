Imports System.Collections.Generic
Module Check
    Dim x As Object = New HashSet(Of Object) From {
        "apple",  ' inline comment
        ' before banana
        "banana"
        ' trailing
    }
End Module
