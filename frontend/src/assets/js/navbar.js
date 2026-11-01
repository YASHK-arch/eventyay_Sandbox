// Navbar helper script – handles outside‑click detection for dropdowns
// Previously used a generic 'click' listener which also fired for keyboard
// activation (Enter key) causing the dropdowns to close immediately.
// The listener is now attached to 'mousedown' (or 'pointerdown' where supported)
// so that keyboard events no longer trigger the outside‑click logic.

(function () {
  // Utility to determine if an element is inside a dropdown toggle
  function isInsideDropdown(el) {
    return el.closest && el.closest('.dropdown-toggle') !== null;
  }

  // Close any open dropdowns when clicking outside of them
  function handleOutsideClick(event) {
    if (isInsideDropdown(event.target)) {
      // Click originated from a dropdown toggle – let Bootstrap‑Vue handle it
      return;
    }
    // Dispatch a custom event that Bootstrap‑Vue dropdowns listen for to close
    var closeEvent = new CustomEvent('bv::dropdown::hide', { bubbles: true });
    document.dispatchEvent(closeEvent);
  }

  // Use 'mousedown' instead of 'click' to avoid reacting to keyboard Enter/Space
  var outsideEvent = 'mousedown';
  if (window.PointerEvent) {
    outsideEvent = 'pointerdown';
  }

  document.addEventListener(outsideEvent, handleOutsideClick);
})();
