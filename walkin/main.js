// HackHarvard Walk-In Confirmation - Interaction Logic
(function () {
  const openWaiverBtn = document.getElementById('openWaiverBtn');
  const waiverDownloadLink = document.getElementById('waiverDownloadLink');
  const acceptWaiver = document.getElementById('acceptWaiver');
  const mediaRelease = document.getElementById('mediaRelease');
  const finalDecision = document.getElementById('finalDecision');
  const submitBtn = document.getElementById('submitBtn');
  const form = document.getElementById('confirmForm');
  const errorText = document.getElementById('errorText');
  const confirmationScreen = document.getElementById('confirmationScreen');
  const confirmTimestamp = document.getElementById('confirmTimestamp');
  const backBtn = document.getElementById('backBtn');

  // Helper: format current time nicely in local timezone
  function formatNow() {
    const now = new Date();
    return now.toLocaleString(undefined, {
      year: 'numeric', month: 'short', day: '2-digit',
      hour: '2-digit', minute: '2-digit', second: '2-digit'
    });
  }

  // Enable waiver checkbox only after opening PDF
  openWaiverBtn?.addEventListener('click', () => {
    const pdfUrl = './walkin_waiver.pdf';
    // Try opening in a new tab
    const win = window.open(pdfUrl, '_blank', 'noopener');
    if (!win) {
      // Popup blocked; reveal a direct link
      waiverDownloadLink.hidden = false;
    }
    // Enable acceptance regardless (we cannot detect if they actually read it)
    acceptWaiver.disabled = false;
    acceptWaiver.focus();
  });

  // Validation: all required checkboxes must be checked
  function validate() {
    const ok = acceptWaiver.checked && mediaRelease.checked && finalDecision.checked;
    submitBtn.disabled = !ok;
    if (ok) {
      errorText.hidden = true;
    }
    return ok;
  }

  [acceptWaiver, mediaRelease, finalDecision].forEach(el => {
    el.addEventListener('change', validate);
  });

  form?.addEventListener('submit', (e) => {
    e.preventDefault();
    const ok = validate();
    if (!ok) {
      errorText.hidden = false;
      errorText.textContent = 'Please complete all required steps before submitting.';
      return;
    }

    // Show confirmation screen
    confirmTimestamp.textContent = formatNow();
    confirmationScreen.hidden = false;

    // Optionally disable the form's controls to prevent resubmission
    Array.from(form.querySelectorAll('input, button')).forEach(el => el.disabled = true);
    submitBtn.textContent = 'Confirmed';
    submitBtn.classList.remove('btn-success');
  });

  backBtn?.addEventListener('click', () => {
    // Allow user to go back if needed (does not undo finality notice, just UI)
    confirmationScreen.hidden = true;
    Array.from(form.querySelectorAll('input')).forEach(el => el.disabled = false);
    validate();
  });

  // Initial state
  validate();
})();
