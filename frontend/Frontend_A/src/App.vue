<template>
  <div id="app">
    <Navbar />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'

export default {
  name: 'App',
  components: {
    Navbar
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  background-color: #f5f5f5;
}

.main-content {
  min-height: calc(100vh - 60px);
  padding: 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.form-container {
  max-width: 400px;
  margin: 40px auto;
}

.page-title {
  text-align: center;
  margin-bottom: 30px;
  color: #303133;
  font-size: 24px;
  font-weight: 600;
}
</style> 