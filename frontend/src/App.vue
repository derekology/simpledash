<script setup lang="ts">

function goToWebsite() {
  window.open('https://derekw.co/?utm_medium=referral&utm_source=simple-pixel', '_blank');
}
</script>

<template>
  <header class="top-bar">
    <h1 class="logo"><span class="logo-highlight">::</span>simple dash<span class="byline" @click="goToWebsite">by
        derekw</span></h1>
    <div class="nav">
      <button class="nav-button" title="Upload">
        upload
      </button>
      <button class="nav-button" title="Dashboard">
        dashboard
      </button>
      <button class="nav-button delete-button" title="Help">
        help
      </button>
    </div>
  </header>

  <RouterView />
</template>

<style>
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--color-bg-dark);
  color: var(--color-text-white);
  box-shadow: var(--shadow-md);
  ;
  border-top: 5px solid var(--color-primary);
  height: var(--top-bar-height);
}

.logo {
  pointer-events: none;
  user-select: none;
  margin: var(--spacing-sm) 0.75rem;
  font-size: 1.25rem;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.logo-highlight {
  color: var(--color-primary);
  font-weight: 900;
  margin-right: var(--radius-sm);
  font-size: 0.75rem;
}

.byline {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  margin-left: var(--radius-sm);
  cursor: pointer;
  pointer-events: auto;
  font-style: italic;
  transition: var(--transition-normal);
}

.byline:hover {
  color: var(--color-text-white);
}

.nav {
  display: flex;
  align-items: center;
  height: 100%;
}

.nav-button {
  min-width: 100px;
  padding: var(--spacing-sm) 0.75rem;
  height: 100%;
  border: 0;
  background: var(--color-bg-dark);
  color: var(--color-text-white);
  cursor: pointer;
  transition: var(--transition-normal);
}

.nav-button:hover {
  background: var(--color-bg-hover);
}
</style>
