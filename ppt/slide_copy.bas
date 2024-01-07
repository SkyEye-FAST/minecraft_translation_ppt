Sub slide_copy()
    Dim i As Integer
    Dim slideCount As Integer

    slideCount = ActivePresentation.Slides.Count

    For i = 1 To 1044
        ActivePresentation.Slides(slideCount).Copy
        ActivePresentation.Slides.Paste
    Next i
End Sub

