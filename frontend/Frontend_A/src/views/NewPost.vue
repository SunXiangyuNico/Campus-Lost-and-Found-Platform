<template>
  <div class="container">
    <div class="form-container">
      <div class="card">
        <h2 class="page-title">发布信息</h2>
        
        <el-form
          ref="postFormRef"
          :model="postForm"
          :rules="postRules"
          label-width="100px"
        >
          <el-form-item label="信息类型" prop="status">
            <el-radio-group v-model="postForm.status">
              <el-radio label="lost">失物</el-radio>
              <el-radio label="found">拾物</el-radio>
            </el-radio-group>
          </el-form-item>
          
          <el-form-item label="物品名称" prop="title">
            <el-input
              v-model="postForm.title"
              placeholder="请输入物品名称"
              clearable
            />
          </el-form-item>
          
          <el-form-item label="物品描述" prop="description">
            <el-input
              v-model="postForm.description"
              type="textarea"
              :rows="4"
              placeholder="请详细描述物品特征、丢失/拾获地点等信息"
              clearable
            />
          </el-form-item>
          
          <el-form-item label="丢失/拾获地点" prop="location">
            <el-input
              v-model="postForm.location"
              placeholder="请输入具体地点"
              clearable
            />
          </el-form-item>
          
          <el-form-item label="时间" prop="date">
            <el-date-picker
              v-model="postForm.date"
              type="datetime"
              placeholder="选择日期时间"
              format="YYYY-MM-DD HH:mm"
              value-format="YYYY-MM-DD HH:mm:ss"
            />
          </el-form-item>
          
          <el-form-item label="物品图片">
            <Uploader v-model="postForm.imageUrl" />
          </el-form-item>
          
          <el-form-item label="联系方式" prop="contact">
            <el-input
              v-model="postForm.contact"
              placeholder="请输入联系方式（手机号、微信等）"
              clearable
            />
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="primary"
              :loading="isSubmitting"
              @click="handleSubmit"
            >
              发布信息
            </el-button>
            <el-button @click="$router.go(-1)">取消</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import Uploader from '@/components/Uploader.vue'
import { createItem } from '@/api/items.js'

export default {
  name: 'NewPost',
  components: {
    Uploader
  },
  setup() {
    const router = useRouter()
    const postFormRef = ref()
    const isSubmitting = ref(false)

    const postForm = reactive({
      status: 'lost',
      title: '',
      description: '',
      location: '',
      date: '',
      imageUrl: '',
      contact: ''
    })

    const postRules = {
      status: [
        { required: true, message: '请选择信息类型', trigger: 'change' }
      ],
      title: [
        { required: true, message: '请输入物品名称', trigger: 'blur' },
        { min: 2, max: 50, message: '物品名称长度在 2 到 50 个字符', trigger: 'blur' }
      ],
      description: [
        { required: true, message: '请输入物品描述', trigger: 'blur' },
        { min: 10, max: 500, message: '描述长度在 10 到 500 个字符', trigger: 'blur' }
      ],
      location: [
        { required: true, message: '请输入地点', trigger: 'blur' }
      ],
      date: [
        { required: true, message: '请选择时间', trigger: 'change' }
      ],
      contact: [
        { required: true, message: '请输入联系方式', trigger: 'blur' }
      ]
    }

    const handleSubmit = async () => {
      try {
        await postFormRef.value.validate()
        isSubmitting.value = true
        
        const result = await createItem(postForm)
        
        if (result.success) {
          ElMessage.success('发布成功')
          router.push('/')
        } else {
          ElMessage.error(result.error || '发布失败')
        }
      } catch (error) {
        console.error('发布失败:', error)
        ElMessage.error('发布失败，请重试')
      } finally {
        isSubmitting.value = false
      }
    }

    return {
      postFormRef,
      postForm,
      postRules,
      isSubmitting,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.form-container {
  max-width: 600px;
  margin: 40px auto;
}
</style> 