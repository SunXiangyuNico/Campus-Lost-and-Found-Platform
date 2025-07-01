<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-card">
        <div class="register-header">
          <h2>注册</h2>
          <p>加入校园失物招领平台</p>
        </div>

        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-width="80px"
        >
          <el-form-item label="学号" prop="studentId">
            <el-input
              v-model="form.studentId"
              placeholder="请输入学号（8-12位数字）"
              clearable
            />
          </el-form-item>

          <el-form-item label="昵称" prop="nickname">
            <el-input
              v-model="form.nickname"
              placeholder="请输入昵称（不超过20字）"
              maxlength="20"
              show-word-limit
              clearable
            />
          </el-form-item>

          <el-form-item label="密码" prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码（至少6位）"
              show-password
              clearable
            />
          </el-form-item>

          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input
              v-model="form.confirmPassword"
              type="password"
              placeholder="请再次输入密码"
              show-password
              clearable
            />
          </el-form-item>

          <el-form-item label="头像" prop="avatar">
            <el-upload
              ref="uploadRef"
              :file-list="fileList"
              :auto-upload="false"
              :on-change="handleAvatarChange"
              :before-upload="beforeAvatarUpload"
              list-type="picture-card"
              :limit="1"
              accept="image/*"
            >
              <el-icon><Plus /></el-icon>
            </el-upload>
            <div class="upload-tip">
              支持jpg、png格式，最大2MB
            </div>
          </el-form-item>

          <el-form-item label="联系方式">
            <el-input
              v-model="form.contact"
              placeholder="电话或邮箱（可选）"
              clearable
            />
          </el-form-item>

          <el-form-item label="学院">
            <el-input
              v-model="form.college"
              placeholder="学院/系别（可选）"
              clearable
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              @click="handleSubmit"
              style="width: 100%"
            >
              注册
            </el-button>
          </el-form-item>
        </el-form>

        <div class="register-footer">
          <span>已有账号？</span>
          <el-button type="text" @click="$router.push('/login')">
            立即登录
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { Plus } from '@element-plus/icons-vue'
import { useUserStore } from '../stores/user'
import { authService } from '../api/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref()
const uploadRef = ref()
const loading = ref(false)
const fileList = ref([])

const form = reactive({
  studentId: '',
  nickname: '',
  password: '',
  confirmPassword: '',
  avatar: null,
  contact: '',
  college: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== form.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  studentId: [
    { required: true, message: '请输入学号', trigger: 'blur' },
    { pattern: /^\d{8,12}$/, message: '学号格式不正确（8-12位数字）', trigger: 'blur' }
  ],
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 1, max: 20, message: '昵称长度在1到20个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ],
  avatar: [
    { required: true, message: '请上传头像', trigger: 'change' }
  ]
}

const handleAvatarChange = (file, fileList) => {
  fileList.value = fileList
  if (fileList.length > 0) {
    form.avatar = fileList[0].raw
  }
}

const beforeAvatarUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过2MB!')
    return false
  }
  return false // 阻止自动上传
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    
    if (!form.avatar) {
      ElMessage.warning('请上传头像')
      return
    }

    loading.value = true

    const userData = {
      studentId: form.studentId,
      nickname: form.nickname,
      password: form.password,
      avatar: form.avatar,
      contact: form.contact,
      college: form.college
    }

    const response = await authService.register(userData)
    
    // 注册成功，自动登录
    userStore.login(response.user, response.token)
    
    ElMessage.success('注册成功！')
    router.push('/')
  } catch (error) {
    console.error('注册失败:', error)
    ElMessage.error(error.response?.data?.message || '注册失败，请重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.register-container {
  width: 100%;
  max-width: 500px;
}

.register-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  padding: 40px;
}

.register-header {
  text-align: center;
  margin-bottom: 32px;
}

.register-header h2 {
  color: #303133;
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 600;
}

.register-header p {
  color: #909399;
  margin: 0;
  font-size: 14px;
}

.upload-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
}

.register-footer {
  text-align: center;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
  color: #909399;
  font-size: 14px;
}

.register-footer .el-button {
  margin-left: 8px;
}
</style> 