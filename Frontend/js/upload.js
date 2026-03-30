const uploadForm = document.getElementById('uploadForm');
const resumeFiles = document.getElementById('resumeFiles');
const jobDescription = document.getElementById('jobDescription');
const uploadStatus = document.getElementById('uploadStatus');
const fileNamesDiv = document.getElementById('file-names');

resumeFiles.addEventListener('change', () => {
    const files = Array.from(resumeFiles.files).map(f => f.name).join(', ');
    fileNamesDiv.textContent = files || "No file selected";
});

uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    if(resumeFiles.files.length === 0 || jobDescription.value.trim() === "") {
        alert("Upload resumes and enter job description!");
        return;
    }

    const formData = new FormData();
    for(let i=0; i<resumeFiles.files.length; i++){
        formData.append('resumes', resumeFiles.files[i]);
    }
    formData.append('job_description', jobDescription.value);

    uploadStatus.textContent = "Analyzing resumes... ⏳";

    try {
        const token = localStorage.getItem("token");
        const response = await fetch('http://localhost:8000/analyze', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData
        });

        const data = await response.json();

        if(response.ok){
            localStorage.setItem('results', JSON.stringify(data.top_10));
            uploadStatus.textContent = "✅ Analysis done! Redirecting...";
            setTimeout(() => { window.location.href = "dashboard.html"; }, 1500);
        } else {
            uploadStatus.textContent = "❌ " + (data.detail || JSON.stringify(data));
        }

    } catch(err){
        console.error(err);
        uploadStatus.textContent = "❌ Server error. Try again!";
    }
});