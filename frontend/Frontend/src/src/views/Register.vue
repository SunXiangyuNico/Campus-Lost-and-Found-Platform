<template>
  <el-dialog :model-value="visible" @update:model-value="onDialogVisible" width="440px" :show-close="true" center title="用户注册" @close="onClose">
    <el-form :model="form" :rules="rules" ref="formRef" label-width="90px" size="large">
      <el-form-item label="姓名" prop="name">
        <el-input v-model="form.name" maxlength="20" show-word-limit placeholder="请输入姓名" />
      </el-form-item>
      <el-form-item label="学号" prop="studentId">
        <el-input v-model="form.studentId" maxlength="12" show-word-limit placeholder="请输入学号（8-12位数字）" />
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
      </el-form-item>
      <el-form-item label="电话" prop="phone">
        <el-input v-model="form.phone" maxlength="15" placeholder="请输入联系电话" />
      </el-form-item>
      <el-form-item label="微信号" prop="wechat">
        <el-input v-model="form.wechat" maxlength="30" placeholder="请输入微信号" />
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
const props = defineProps({
  visible: Boolean
})
const emit = defineEmits(['update:visible', 'switch-login'])
const formRef = ref()
const form = ref({
  name: '',
  studentId: '',
  password: '',
  phone: '',
  wechat: ''
})
const rules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  studentId: [
    { required: true, message: '请输入学号', trigger: 'blur' },
    { pattern: /^\d{8,12}$/, message: '学号为8-12位数字', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^\d{6,15}$/, message: '电话为6-15位数字', trigger: 'blur' }
  ],
  wechat: [
    { required: true, message: '请输入微信号', trigger: 'blur' }
  ]
}
function onRegister() {
  formRef.value.validate(valid => {
    if (!valid) return
    // 注册逻辑，成功后关闭弹窗
    ElMessage.success('注册成功')
    emit('update:visible', false)
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