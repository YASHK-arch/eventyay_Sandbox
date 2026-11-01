<template>
  <b-navbar toggleable="lg" type="dark" variant="primary">
    <b-navbar-brand href="#">Eventyay</b-navbar-brand>

    <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

    <b-collapse id="nav_collapse" is-nav>
      <b-navbar-nav class="ml-auto">
        <!-- Language Dropdown -->
        <b-dropdown
          id="langDropdown"
          ref="langMenu"
          right
          toggle-class="nav-link"
          no-caret
          auto-close="outside"
          @keydown.enter.stop.prevent="$event.target.click()"
          @keydown.space.stop.prevent="$event.target.click()"
          @keydown.esc="closeLangMenu"
        >
          <template #button-content>
            {{ $t('Language') }}
          </template>
          <b-dropdown-item @click="setLocale('en')">English</b-dropdown-item>
          <b-dropdown-item @click="setLocale('de')">Deutsch</b-dropdown-item>
          <!-- Add more languages as needed -->
        </b-dropdown>

        <!-- Profile Dropdown -->
        <b-dropdown
          id="profileDropdown"
          ref="profileMenu"
          right
          toggle-class="nav-link"
          no-caret
          auto-close="outside"
          @keydown.enter.stop.prevent="$event.target.click()"
          @keydown.space.stop.prevent="$event.target.click()"
          @keydown.esc="closeProfileMenu"
        >
          <template #button-content>
            <i class="fa fa-user" aria-hidden="true"></i>
          </template>
          <b-dropdown-item href="/profile">{{ $t('Profile') }}</b-dropdown-item>
          <b-dropdown-item href="/logout">{{ $t('Logout') }}</b-dropdown-item>
        </b-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
export default {
  methods: {
    setLocale(locale) {
      // Existing locale‑switching logic (unchanged)
      this.$i18n.locale = locale;
    },
    closeLangMenu() {
      // Programmatically close the language dropdown if it is open
      if (this.$refs.langMenu && this.$refs.langMenu.visible) {
        this.$refs.langMenu.hide(true);
      }
    },
    closeProfileMenu() {
      // Programmatically close the profile dropdown if it is open
      if (this.$refs.profileMenu && this.$refs.profileMenu.visible) {
        this.$refs.profileMenu.hide(true);
      }
    }
  }
};
</script>
