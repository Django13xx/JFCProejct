<template>
  <div>
    <nav class="navbar">
      <div class="nav-item">
        <router-link to="/mainPage" class="nav-link"  exact active-class="active-link">Practice</router-link>
      </div>
      <div class="nav-item">
        <router-link to="/login" class="nav-link"  exact active-class="active-link">Start</router-link>
      </div>
      <div class="nav-item">
        <router-link to="/teachingDashboard" class="nav-link"  exact active-class="active-link">Teaching</router-link>
      </div>
      <div class="nav-item">
        <router-link to="/help" class="nav-link"  exact active-class="active-link">Help</router-link>
      </div>
    </nav>
    <router-view></router-view>
  </div>
</template>

<style scoped>
.navbar {
  background-color: #4c4b4b; /* grey background */
  display: flex;
  justify-content: space-around;
  padding: 10px;
}

.nav-item {
  /* Make sure the guide bar take enough space */
  flex: 1;
}

.nav-link {
  display: block;
  padding: 10px;
  text-align: center;
  color: #e64626; /* Orange Colour */
  text-decoration: none;
  transition: color 0.3s ease-in-out;
}

.nav-link:hover {
  color: #fff; /* mouse hover to change colour */
  background-color: #4c4b4b; /* mouse hover to change colour */
}

.active-link {
  color: #fff; /* Set the active link color */
  background-color: #e64626; /* Set the active link background color */
}
</style>

export default {
  name: 'MainLayout',
  components: {
    Navbar
  }
}