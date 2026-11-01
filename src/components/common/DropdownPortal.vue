<template>
  <teleport to="#portal-root">
    <div class="dropdown-portal" :style="portalStyle">
      <slot />
    </div>
  </teleport>
</template>

<script>
export default {
  name: "DropdownPortal",
  props: {
    /**
     * Optional inline style object to position the portal (e.g., top, left).
     * The parent component can compute the exact coordinates based on the trigger element.
     */
    portalStyle: {
      type: Object,
      default: () => ({})
    }
  }
};
</script>

<style scoped>
/* Ensure the portal container does not interfere with layout */
.dropdown-portal {
  /* The class also gets the global .dropdown-portal rules, but we keep it scoped for safety */
}
</style>