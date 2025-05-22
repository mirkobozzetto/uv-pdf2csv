from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import tabula
import tempfile
import os

app = FastAPI()

@app.post("/convert")
async def convert(pdf: UploadFile = File(...)):
    tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp_pdf.write(await pdf.read())
    tmp_pdf.close()
    tmp_csv = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    tmp_csv.close()
    tabula.convert_into(tmp_pdf.name, tmp_csv.name, output_format="csv", pages="all", lattice=True)
    os.unlink(tmp_pdf.name)
    return StreamingResponse(open(tmp_csv.name, "rb"), media_type="text/csv", headers={"Content-Disposition": f"attachment; filename=\"{os.path.splitext(pdf.filename)[0]}.csv\""})
