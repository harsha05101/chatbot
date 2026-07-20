import { useDropzone } from "react-dropzone";
import { useState } from "react";

function UploadBox({ onFile }) {
    const [preview, setPreview] = useState(null);

    const { getRootProps, getInputProps } = useDropzone({
        accept: {
            "image/*": []
        },
        onDrop: files => {
            const file = files[0];
            setPreview(URL.createObjectURL(file));
            onFile(file);
        }
    });

    return (
        <div {...getRootProps()} className="upload-box">
            <input {...getInputProps()} />

            {preview ? (
                <img src={preview} alt="preview" width="250" />
            ) : (
                <p>📎 Drag image here or click to upload</p>
            )}
        </div>
    );
}

export default UploadBox;