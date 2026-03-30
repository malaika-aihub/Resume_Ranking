const downloadBtn = document.getElementById('downloadPDF');

if (downloadBtn) {
  downloadBtn.addEventListener('click', async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await fetch('http://localhost:8000/download_resume/Top10_Resume_Report.pdf', {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if(response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'Top10_Resume_Report.pdf';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      } else {
        alert("PDF download failed.");
      }
    } catch (err) {
      console.error(err);
      alert("Server error. Try again!");
    }
  });
}