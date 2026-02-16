// Get results from localStorage
const candidateCards = document.getElementById('candidateCards');
const topCandidates = JSON.parse(localStorage.getItem('results') || '[]');

if(topCandidates.length === 0) {
  candidateCards.innerHTML = "<p>No data found. Go back and upload resumes.</p>";
} else {
  topCandidates.forEach((candidate, index) => {
    const card = document.createElement('div');
    card.className = "candidate-card";
    card.innerHTML = `
      <h3>${index + 1}. ${candidate.name}</h3>
      <p>Match Score: ${candidate.match_score}%</p>
      <p>Skills: ${candidate.skills.join(', ')}</p>
      <p>Experience: ${candidate.experience} years</p>
      <a href="${candidate.resume_url}" target="_blank">View Resume</a>
    `;
    candidateCards.appendChild(card);
  });
}
