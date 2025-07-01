<template>
  <el-dialog
    v-model="visible"
    title="发布失物/招领"
    width="600px"
    :before-close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="80px"
    >
      <el-form-item label="类型" prop="type">
        <el-radio-group v-model="form.type">
          <el-radio label="lost">失物</el-radio>
          <el-radio label="found">招领</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="标题" prop="title">
        <el-input
          v-model="form.title"
          placeholder="请输入标题"
          maxlength="50"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="地点" prop="location">
        <el-input
          v-model="form.location"
          placeholder="例如：教学楼3楼走廊"
        />
      </el-form-item>

      <el-form-item label="描述" prop="description">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="4"
          placeholder="请详细描述物品特征、丢失/拾取经过等信息"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="图片">
        <el-upload
          ref="uploadRef"
          :file-list="fileList"
          :auto-upload="false"
          :on-change="handleFileChange"
          :on-remove="handleFileRemove"
          :before-upload="beforeUpload"
          list-type="picture-card"
          :limit="5"
          accept="image/*"
        >
          <el-icon><Plus /></el-icon>
        </el-upload>
        <div class="upload-tip">
          支持jpg、png格式，单张不超过2MB，最多5张
        </div>
      </el-form-item>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="loading">
          发布
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { postsService } from '../api/posts'
import { usePostsStore } from '../stores/posts'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'success'])

const visible = ref(props.modelValue)
const loading = ref(false)
const formRef = ref()
const uploadRef = ref()
const fileList = ref([])

const form = reactive({
  type: 'lost',
  title: '',
  location: '',
  description: '',
  images: []
})

const rules = {
  type: [
    { required: true, message: '请选择类型', trigger: 'change' }
  ],
  title: [
    { required: true, message: '请输入标题', trigger: 'blur' },
    { min: 2, max: 50, message: '标题长度在2到50个字符', trigger: 'blur' }
  ],
  location: [
    { required: true, message: '请输入地点', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入描述', trigger: 'blur' },
    { min: 10, max: 500, message: '描述长度在10到500个字符', trigger: 'blur' }
  ]
}

// 监听visible变化
watch(() => props.modelValue, (val) => {
  visible.value = val
})

watch(visible, (val) => {
  emit('update:modelValue', val)
  if (!val) {
    resetForm()
  }
})

const handleFileChange = (file, fileList) => {
  fileList.value = fileList
  if (fileList.length > 0) {
    form.images = fileList.map(f => f.raw)
  }
}

const handleFileRemove = (file, fileList) => {
  fileList.value = fileList
  form.images = fileList.map(f => f.raw)
}

const beforeUpload = (file) => {
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
    
    // 检查图片数量
    if (fileList.value.length === 0) {
      ElMessage.warning('请至少上传一张图片')
      return
    }

    loading.value = true

    // 准备表单数据
    const formData = {
      ...form,
      images: fileList.value.map(file => file.raw),
      latitude: 39.9042, // 默认坐标，实际应用中应该通过地图选择
      longitude: 116.4074
    }

    const result = await postsService.createPost(formData)
    
    // 添加到store
    const postsStore = usePostsStore()
    postsStore.addPost(result)
    postsStore.setCurrentPost(result)
    
    ElMessage.success('发布成功')
    emit('success', result)
    handleClose()
  } catch (error) {
    console.error('发布失败:', error)
    ElMessage.error('发布失败，请重试')
  } finally {
    loading.value = false
  }
}

const handleClose = () => {
  visible.value = false
}

const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  fileList.value = []
  form.images = []
}
</script>

<style scoped>
.upload-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style> 