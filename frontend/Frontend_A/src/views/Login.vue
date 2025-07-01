<template>
  <div class="container">
    <div class="form-container">
      <div class="card">
        <h2 class="page-title">用户登录</h2>
        
        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          label-width="80px"
          @submit.prevent="handleLogin"
        >
          <el-form-item label="用户名" prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              prefix-icon="User"
              clearable
            />
          </el-form-item>
          
          <el-form-item label="密码" prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              prefix-icon="Lock"
              show-password
              clearable
            />
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="primary"
              :loading="userStore.isLoading"
              @click="handleLogin"
              style="width: 100%"
            >
              登录
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="form-footer">
          <span>还没有账号？</span>
          <router-link to="/register" class="link">立即注册</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user.js'
import { ElMessage } from 'element-plus'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    const loginFormRef = ref()

    const loginForm = reactive({
      username: '',
      password: ''
    })

    const loginRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
      ]
    }

    const handleLogin = async () => {
      try {
        await loginFormRef.value.validate()
        
        const result = await userStore.login(loginForm)
        
        if (result.success) {
          ElMessage.success('登录成功')
          router.push('/')
        } else {
          ElMessage.error(result.error)
        }
      } catch (error) {
        console.error('登录失败:', error)
        ElMessage.error('登录失败，请重试')
      }
    }

    return {
      loginFormRef,
      loginForm,
      loginRules,
      userStore,
      handleLogin
    }
  }
}
</script>

<style scoped>
.form-container {
  max-width: 400px;
  margin: 40px auto;
}

.form-footer {
  text-align: center;
  margin-top: 20px;
  color: #606266;
}

.link {
  color: #409eff;
  text-decoration: none;
  margin-left: 5px;
}

.link:hover {
  text-decoration: underline;
}
</style> 