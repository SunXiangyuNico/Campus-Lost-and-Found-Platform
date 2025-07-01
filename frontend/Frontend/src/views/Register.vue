<template>
  <div class="register-container">
    <el-card class="register-card">
      <h2 class="title">用户注册</h2>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="90px" size="large">
        <el-form-item label="学号" prop="studentId">
          <el-input v-model="form.studentId" maxlength="12" show-word-limit placeholder="请输入学号（8-12位数字）" />
        </el-form-item>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="form.nickname" maxlength="20" show-word-limit placeholder="请输入昵称（不超过20字）" />
        </el-form-item>
        <el-form-item label="头像" prop="avatar">
          <el-upload
            class="avatar-uploader"
            action="#"
            :show-file-list="false"
            :before-upload="beforeAvatarUpload"
            :on-change="handleAvatarChange"
          >
            <img v-if="form.avatarUrl" :src="form.avatarUrl" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="联系方式" prop="contact">
          <el-input v-model="form.contact" placeholder="电话或邮箱（可选）" />
        </el-form-item>
        <el-form-item label="学院/系别" prop="college">
          <el-input v-model="form.college" placeholder="请输入学院/系别（可选）" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="form.confirmPassword" type="password" placeholder="请再次输入密码" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit" :loading="loading" style="width:100%">注册</el-button>
        </el-form-item>
        <el-form-item>
          <span>已有账号？<router-link to="/login">去登录</router-link></span>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { register } from '../api/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const formRef = ref()
const loading = ref(false)
const form = ref({
  studentId: '',
  nickname: '',
  avatar: null,
  avatarUrl: '',
  contact: '',
  college: '',
  password: '',
  confirmPassword: ''
})

const rules = {
  studentId: [
    { required: true, message: '请输入学号', trigger: 'blur' },
    { pattern: /^\d{8,12}$/, message: '学号为8-12位数字', trigger: 'blur' }
  ],
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { max: 20, message: '昵称不超过20字', trigger: 'blur' }
  ],
  avatar: [
    { required: true, message: '请上传头像', trigger: 'change' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: (rule, value) => value === form.value.password, message: '两次输入密码不一致', trigger: 'blur' }
  ]
}

function beforeAvatarUpload(file) {
  const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2
  if (!isJpgOrPng) {
    ElMessage.error('头像仅支持 jpg/png 格式!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('头像大小不能超过 2MB!')
    return false
  }
  return true
}
function handleAvatarChange(file) {
  const reader = new FileReader()
  reader.onload = e => {
    form.value.avatarUrl = e.target.result
    form.value.avatar = file.raw
  }
  reader.readAsDataURL(file.raw)
}

async function onSubmit() {
  await formRef.value.validate(async valid => {
    if (!valid) return
    loading.value = true
    try {
      // 这里只上传 base64，实际应上传到后端获取url
      const payload = { ...form.value, avatar: form.value.avatarUrl }
      await register(payload)
      ElMessage.success('注册成功，正在跳转首页...')
      router.push('/')
    } catch (e) {
      ElMessage.error(e?.response?.data?.message || '注册失败')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f7f8fa;
}
.register-card {
  width: 420px;
  padding: 32px 36px 12px 36px;
  border-radius: 12px;
  box-shadow: 0 4px 24px #e6e8f0;
}
.title {
  text-align: center;
  margin-bottom: 24px;
  font-weight: bold;
  font-size: 24px;
}
.avatar-uploader {
  display: flex;
  align-items: center;
  justify-content: flex-start;
}
.avatar-uploader-icon {
  font-size: 32px;
  color: #999;
  border: 1px dashed #d9d9d9;
  border-radius: 50%;
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafafa;
}
.avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #eee;
}
</style> 