<template>
  <main>
    <section>
      <base-card>
        <h2>Page Not Found!</h2>
        <p>
          This Page could not be found. Go back to
          <router-link to="/base">Admin Panel?</router-link>
        </p>
      </base-card>
    </section>
  </main>
</template>

<style scoped>
section {
    display: flex;
    justify-content: center;
}
</style>
