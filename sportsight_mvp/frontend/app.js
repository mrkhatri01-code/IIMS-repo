// === Simple Frontend Logic for SportSight MVP ===

const uploadForm = document.getElementById('upload-form');
const videoInput = document.getElementById('video-input');
const runBtn = document.getElementById('run-btn');
const statusMsg = document.getElementById('status-msg');
const resultsSection = document.getElementById('results-section');
const resultsList = document.getElementById('results-list');

let uploaded = false;
let processing = false;

// --- Upload Video ---
uploadForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const file = videoInput.files[0];
  if (!file) return;
  statusMsg.textContent = 'Uploading video...';
  runBtn.disabled = true;

  const formData = new FormData();
  formData.append('video', file);

  try {
    const res = await fetch('/upload', {
      method: 'POST',
      body: formData,
    });
    if (res.ok) {
      statusMsg.textContent = 'Video uploaded! Ready to generate highlights.';
      runBtn.disabled = false;
      uploaded = true;
    } else {
      // Try to get error message from backend
      let errorMsg = 'Upload failed. Please try again.';
      try {
        const text = await res.text();
        if (text) errorMsg = `Upload failed: ${text}`;
      } catch {}
      statusMsg.textContent = errorMsg;
    }
  } catch (err) {
    statusMsg.textContent = 'Error uploading video.';
  }
});

// --- Run Highlight Generator ---
runBtn.addEventListener('click', async () => {
  if (!uploaded || processing) return;
  statusMsg.textContent = 'Processing video for highlights...';
  runBtn.disabled = true;
  processing = true;

  try {
    const res = await fetch('/run', { method: 'POST' });
    if (res.ok) {
      statusMsg.textContent = 'Processing complete! Fetching results...';
      await fetchResults();
    } else {
      statusMsg.textContent = 'Processing failed. Please try again.';
    }
  } catch (err) {
    statusMsg.textContent = 'Error running highlight generator.';
  }
  processing = false;
});

// --- Fetch and Display Results ---
async function fetchResults() {
  try {
    const res = await fetch('/results');
    if (!res.ok) throw new Error('Failed to fetch results');
    const data = await res.json();
    if (!Array.isArray(data) || data.length === 0) {
      statusMsg.textContent = 'No highlights found.';
      return;
    }
    renderResults(data);
    resultsSection.style.display = '';
    statusMsg.textContent = 'Highlights ready!';
  } catch (err) {
    statusMsg.textContent = 'Error fetching results.';
  }
}

function renderResults(results) {
  resultsList.innerHTML = '';
  results.forEach((item, idx) => {
    const card = document.createElement('div');
    card.className = 'result-card';

    // Video preview
    const video = document.createElement('video');
    video.src = item.clip_url;
    video.controls = true;
    card.appendChild(video);

    // Caption
    const caption = document.createElement('div');
    caption.className = 'caption';
    caption.textContent = item.caption;
    card.appendChild(caption);

    // Download button
    const dlBtn = document.createElement('a');
    dlBtn.href = item.clip_url;
    dlBtn.download = `highlight_${idx+1}.mp4`;
    dlBtn.textContent = 'Download Clip';
    dlBtn.className = 'download-btn';
    card.appendChild(dlBtn);

    resultsList.appendChild(card);
  });
} 