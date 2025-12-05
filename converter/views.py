
from django.shortcuts import render
from django.http import FileResponse
import os
from docx2pdf import convert
from pdf2docx import Converter

def convert_file(request):
    download_url = None

    if request.method == "POST" and request.FILES.get("file"):
        uploaded = request.FILES["file"]
        input_path = "media/input/" + uploaded.name
        output_name = uploaded.name.split('.')[0]

        os.makedirs("media/input", exist_ok=True)
        os.makedirs("media/output", exist_ok=True)

        with open(input_path, "wb") as f:
            for chunk in uploaded.chunks():
                f.write(chunk)

        # PDF → Word
        if uploaded.name.endswith(".pdf"):
            output_path = f"media/output/{output_name}.docx"
            cv = Converter(input_path)
            cv.convert(output_path)
            cv.close()

        # Word → PDF
        elif uploaded.name.endswith(".docx"):
            output_path = f"media/output/{output_name}.pdf"
            convert(input_path, output_path)

        download_url = "/" + output_path

    return render(request, "home.html", {"download_url": download_url})

