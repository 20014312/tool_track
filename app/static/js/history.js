document.querySelectorAll('.toggle-heading').forEach(heading => {
    heading.addEventListener('click', () => {
      const content = heading.nextElementSibling;
      content.classList.toggle('show');
    });
  });

  function updateRequest(reqId, status) {
    const formData = new FormData();
    formData.append("status", status)
    fetch(`/update-request-status/${reqId}`, {
      method: 'POST',
      body: formData,
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          location.reload();
          document.getElementById(`status-${reqId}`).innerText = status;
        }
      });
  }

  function returnTool(reqId) {
    
    fetch(`/update-request-status/${reqId}`, {
      method: 'POST',
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          location.reload();
          document.getElementById(`status-${reqId}`).innerText = status;
        }
      });
  }