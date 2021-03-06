<template>
    
  <nav class="navbar">
    <ul class="navbar-nav">
        <li class="logo">
            <router-link class="nav-link" to='/'>
                <span class="link-text">Xpert</span>
            </router-link>
        </li>
      <li class="nav-item">
        <router-link class="nav-link" to="/student">
          <img src="~@/assets/graduated.png" />
          <span class="link-text">Students</span>
        </router-link>
      </li>

      <li class="nav-item">
        <router-link class="nav-link" to="/examiner">
          <img src="~@/assets/teacher.png" />
          <span class="link-text">Examiners</span>
        </router-link>
      </li>

      <li class="nav-item">
        <router-link class="nav-link" to="/categories">
          <img src="~@/assets/online-course.png" />
          <span class="link-text">Courses</span>
        </router-link>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
    
}
</script>

<style scoped>
.navbar {
  width: 5rem;
  height: 100vh;
  position: fixed;
  background-color: var(--bg-primary);
  transition: width 200ms ease;
}

.navbar-nav {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
}

.nav-item {
  height: auto;
  width: 100%;
}

.nav-link {
  display: flex;
  align-items: center;
  height: 5rem;
  color: var(--text-primary);
  text-decoration: none;
}

.nav-link:hover {
  color: var(--text-secondary);
}

.link-text {
  display: none;
  margin-left: 3rem;
}

.navbar:hover {
  width: 16rem;
}

.navbar:hover .link-text {
  display: block;
}

.nav-link img {
  width: 2rem;
  min-width: 2rem;
  margin: 0 1.5rem;
}

.logo {
    font-weight: bold;
    text-transform: uppercase;
    margin-bottom: 1rem;
    text-align: center;
    justify-content: center;
    color: var(--text-secondary);
    font-size: 1.5rem;
    letter-spacing: 0.3ch;
    width: 100%;
}
</style>