import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

app = FastAPI(
    debug=True,
    title="test upload", 
    version="1.0.0",
    summary="",
    description="test",
    root_path_in_servers=True,
    include_in_schema=True,
    separate_input_output_schemas=True,
    )


def save_file(file: UploadFile):
    
        folder = os.path.join("/tmp", "documents")
        # Create the directory if it doesn't exist
        if not os.path.exists(folder):
            os.makedirs(folder)  # Create the folder if it doesn't exist
        
        if file.filename:
            file_path = os.path.join(folder, file.filename)
            file_content = file.file.read()        
            with open(file_path, "wb") as f:
                f.write(file_content)
            
            return file_path
        
            
@app.get("/")
async def check_server():
    return {"message": "welcome to test server"}




@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save the file
        file_path = save_file(file)
        
        # Return success response
        return {"filename": file.filename, "status": "uploaded successfully", "file_path": file_path}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download(filename: str):
    try:
        # Download the file
        return download_file(filename)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def download_file(filename: str):
    folder = os.path.join("/tmp", "documents")
    file_path = os.path.join(folder, filename)
    
    # Check if the file exists
    if not os.path.exists(folder):
        raise FileNotFoundError("File not found")

    return FileResponse(file_path)