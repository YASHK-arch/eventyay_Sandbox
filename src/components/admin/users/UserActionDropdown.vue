<template>
  <div class="user-action-dropdown">
    <!-- Trigger button -->
    <bunt-icon-button
      @click="toggle"
      :tooltip="$t('Actions')"
      tooltip-placement="bottom-start"
      :tooltip-fixed="true"
    >
      gear
    </bunt-icon-button>

    <!-- Dropdown menu rendered via portal -->
    <DropdownPortal v-if="open" :portalStyle="computedStyle">
      <ul class="dropdown-menu" @click.stop="" @keydown.stop="">
        <li @click="resendVerification" v-if="!user.is_verified">{{ $t('Resend Verification Email') }}</li>
        <li @click="resetPassword">{{ $t('Reset Password Email') }}</li>
        <!-- other actions -->
      </ul>
    </DropdownPortal>
  </div>
</template>

<script>
import DropdownPortal from "@/components/common/DropdownPortal.vue";

export default {
  name: "UserActionDropdown",
  components: { DropdownPortal },
  props: {
    user: { type: Object, required: true }
  },
  data() {
    return {
      open: false,
      triggerRect: null
    };
  },
  computed: {
    computedStyle() {
      if (!this.triggerRect) return {};
      // Position the portal just below the trigger button, aligned to its left edge.
      return {
        top: `${this.triggerRect.bottom + window.scrollY}px`,
        left: `${this.triggerRect.left + window.scrollX}px`
      };
    }
  },
  methods: {
    toggle(event) {
      this.open = !this.open;
      if (this.open) {
        // Capture the bounding rect of the button to position the portal.
        this.triggerRect = event.currentTarget.getBoundingClientRect();
        document.addEventListener("click", this.handleOutsideClick);
      } else {
        document.removeEventListener("click", this.handleOutsideClick);
      }
    },
    handleOutsideClick(event) {
      if (!this.$el.contains(event.target)) {
        this.open = false;
        document.removeEventListener("click", this.handleOutsideClick);
      }
    },
    resendVerification() {
      this.$emit("resend-verification", this.user);
      this.open = false;
    },
    resetPassword() {
      this.$emit("reset-password", this.user);
      this.open = false;
    }
  }
};
</script>

<style scoped>
.user-action-dropdown {
  position: relative;
}
.dropdown-menu {
  list-style: none;
  margin: 0;
  padding: 0.5rem 0;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  min-width: 150px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}
.dropdown-menu li {
  padding: 0.25rem 1rem;
  cursor: pointer;
}
.dropdown-menu li:hover {
  background: var(--color-bg-hover);
}
</style>