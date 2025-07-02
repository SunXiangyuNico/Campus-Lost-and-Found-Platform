<template>
  <el-dialog :model-value="visible" @update:model-value="onDialogVisible" width="440px" :show-close="true" center title="用户注册" @close="onClose">
    <el-form :model="form" :rules="rules" ref="formRef" label-width="90px" size="large">
      <el-form-item label="姓名" prop="name">
        <el-input v-model="form.name" maxlength="20" show-word-limit placeholder="请输入姓名" />
      </el-form-item>
      <el-form-item label="学号" prop="studentId">
        <el-input v-model="form.studentId" maxlength="12" show-word-limit placeholder="请输入学号（8-12位数字）" />
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="form.email" maxlength="40" placeholder="请输入邮箱" />
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
      </el-form-item>
      <el-form-item label="确认密码" prop="confirmPassword">
        <el-input v-model="form.confirmPassword" type="password" placeholder="确认密码" show-password />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onRegister" style="width:100%">注册</el-button>
      </el-form-item>
      <el-form-item style="text-align:center; width:100%">
        <span>已有账号？<a @click.prevent="$emit('switch-login')" style="color:#409eff;cursor:pointer">去登录</a></span>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'
import { ElMessage } from 'element-plus'
import { register, getUserInfo } from '../api/auth'
import { useUserStore } from '../store/user'
const props = defineProps({
  visible: Boolean
})
const emit = defineEmits(['update:visible', 'switch-login'])
const formRef = ref()
const form = ref({
  name: '',
  studentId: '',
  email: '',
  password: '',
  confirmPassword: ''
})
const rules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  studentId: [
    { required: true, message: '请输入学号', trigger: 'blur' },
    { pattern: /^\d{8,12}$/, message: '学号为8-12位数字', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}
const userStore = useUserStore()

function validateConfirmPassword(rule, value, callback) {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== form.value.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

async function onRegister() {
  formRef.value.validate(async valid => {
    if (!valid) return
    
    try {
      const response = await register({
        username: form.value.name, // 使用姓名作为用户名
        password: form.value.password,
        name: form.value.name,
        studentId: form.value.studentId,
        email: form.value.email
      })
      
      // 保存token和用户信息
      userStore.setToken(response.data.token)
      // 新增：注册后立即拉取用户信息
      const userInfoResp = await getUserInfo(response.data.token)
      userStore.setUserInfo(userInfoResp.data)
      
      ElMessage.success('注册成功')
      emit('update:visible', false)
      
      // 清空表单
      form.value.name = ''
      form.value.studentId = ''
      form.value.email = ''
      form.value.password = ''
      form.value.confirmPassword = ''
    } catch (error) {
      ElMessage.error(error.response?.data?.message || '注册失败')
    }
  })
}
function onClose() {
  emit('update:visible', false)
}
function onDialogVisible(val) {
  emit('update:visible', val)
}
</script>

<style scoped>
</style> 