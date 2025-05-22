#!/usr/bin/env python3
import sys, os, tabula, pandas as pd, csv, tempfile
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse

def convert_cli(pdf_path):
    if not os.path.isfile(pdf_path):
        print("File not found:", pdf_path)
        sys.exit(1)
    base, _ = os.path.splitext(pdf_path)
    csv_path = f"{base}.csv"
    tabula.convert_into(pdf_path, csv_path, output_format="csv", pages="all", lattice=True)  # extraction via Tabula-Py
    df = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")                       # robust reading in Python
    df = df.replace(r"\n", " ", regex=True).fillna("")                                      # remove line breaks
    df.to_csv(csv_path, index=False, quoting=csv.QUOTE_MINIMAL)                            # export with minimal quoting
    print(csv_path)

app = FastAPI()

@app.post("/convert")
async def convert(pdf: UploadFile = File(...)):
    tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp_pdf.write(await pdf.read()); tmp_pdf.close()
    tmp_csv = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    tmp_csv.close()
    tabula.convert_into(tmp_pdf.name, tmp_csv.name, output_format="csv", pages="all", lattice=True)
    os.unlink(tmp_pdf.name)
    df = pd.read_csv(tmp_csv.name, engine="python", on_bad_lines="skip")
    df = df.replace(r"\n", " ", regex=True).fillna("")
    df.to_csv(tmp_csv.name, index=False, quoting=csv.QUOTE_MINIMAL)
    return StreamingResponse(
        open(tmp_csv.name, "rb"),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=\"{os.path.splitext(pdf.filename)[0]}.csv\""}
    )

if __name__ == "__main__":
    if len(sys.argv) == 2:
        convert_cli(sys.argv[1])
    else:
        import uvicorn
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)  # run Uvicorn if no argument
