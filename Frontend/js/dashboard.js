// dashboard.js

const candidateCards = document.getElementById('candidateCards');

// Get top candidates from localStorage
const topCandidates = JSON.parse(localStorage.getItem('results') || '[]');

// Clear container first
candidateCards.innerHTML = "";

// Check if there are candidates
if(topCandidates.length === 0) {
    candidateCards.innerHTML = "<p>No candidates found. Please analyze resumes first.</p>";
} else {
    topCandidates.forEach((candidate, index) => {
        const card = document.createElement('div');
        card.className = "card"; // matches your CSS styling

        // Safely handle missing data
        const name = candidate.name || `Candidate ${index + 1}`;
        const score = candidate.match_score !== undefined ? candidate.match_score : "N/A";
        const skills = candidate.skills && candidate.skills.length ? candidate.skills.join(', ') : "N/A";
        const experience = candidate.experience !== undefined ? candidate.experience : "N/A";
        const resumePath = candidate.resume_path || "#";

        card.innerHTML = `
            <h3>${index + 1}. ${name}</h3>
            <p>Match Score: ${score}%</p>
            <p>Skills: ${skills}</p>
            <p>Experience: ${experience} years</p>
            <a href="${resumePath}" download class="download-btn">Download Resume</a>
        `;

        candidateCards.appendChild(card);
    });
}