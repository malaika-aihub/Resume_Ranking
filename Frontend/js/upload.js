// Select form and inputs
const uploadForm = document.getElementById('uploadForm');
const resumeFiles = document.getElementById('resumeFiles');
const jobDescription = document.getElementById('jobDescription');
const uploadStatus = document.getElementById('uploadStatus');
const fileNamesDiv = document.getElementById('file-names'); // display selected files

// Show selected file names
resumeFiles.addEventListener('change', () => {
    const files = Array.from(resumeFiles.files).map(f => f.name).join(', ');
    fileNamesDiv.textContent = files || "No file selected";
});

uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    if(resumeFiles.files.length === 0 || jobDescription.value.trim() === "") {
        alert("Please upload resumes and enter job description.");
        return;
    }

    const formData = new FormData();
    for(let i=0; i<resumeFiles.files.length; i++) {
        formData.append('resumes', resumeFiles.files[i]);
    }
    formData.append('job_description', jobDescription.value);

    uploadStatus.textContent = "Uploading and analyzing...";

    try {
        const response = await fetch('http://localhost:8000/analyze', {
            method: 'POST',
            headers: { 'api-key': 'YOUR_SECRET_KEY' }, // API key added
            body: formData
        });

        if(response.ok) {
            const data = await response.json();
            // Save data in localStorage for dashboard
            localStorage.setItem('results', JSON.stringify(data.top_10));
            uploadStatus.textContent = "Analysis complete! Redirecting to dashboard...";
            setTimeout(() => {
                window.location.href = "dashboard.html";
            }, 1500);
        } else {
            uploadStatus.textContent = "Error during analysis.";
        }

    } catch (err) {
        console.error(err);
        uploadStatus.textContent = "Server error. Try again!";
    }
});
