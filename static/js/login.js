// Get the modal, button, and span elements
const addUserModal = document.getElementById("addUserModal");
const addUserBtn = document.getElementById("addUserBtn");
const addUserClose = document.getElementsByClassName("close")[0];

// Add event listeners
if (addUserBtn) {
  addUserBtn.onclick = () => {
    addUserModal.style.display = "block";
  };

  addUserClose.onclick = () => {
    addUserModal.style.display = "none";
  };

  window.onclick = (event) => {
    if (event.target === addUserModal) {
      addUserModal.style.display = "none";
    }
  };
}
