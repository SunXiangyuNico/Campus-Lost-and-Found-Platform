<template>
  <div class="uploader">
    <el-upload
      :action="uploadUrl"
      :headers="uploadHeaders"
      :before-upload="beforeUpload"
      :on-success="handleSuccess"
      :on-error="handleError"
      :show-file-list="false"
      accept="image/*"
    >
      <div v-if="!modelValue" class="upload-placeholder">
        <el-icon size="32" color="#c0c4cc"><Plus /></el-icon>
        <p>点击上传图片</p>
      </div>
      <div v-else class="upload-preview">
        <img :src="modelValue" alt="预览" />
        <div class="upload-overlay">
          <el-icon size="24" color="white"><Edit /></el-icon>
        </div>
      </div>
    </el-upload>
    
    <div v-if="modelValue" class="upload-actions">
      <el-button size="small" type="danger" @click="handleRemove">
        删除
      </el-button>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useUserStore } from '@/store/user.js'
import { ElMessage } from 'element-plus'

export default {
  name: 'Uploader',
  props: {
    modelValue: {
      type: String,
      default: ''
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const userStore = useUserStore()

    const uploadUrl = '/api/items/upload'
    
    const uploadHeaders = computed(() => ({
      Authorization: `Bearer ${userStore.token}`
    }))

    const beforeUpload = (file) => {
      const isImage = file.type.startsWith('image/')
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isImage) {
        ElMessage.error('只能上传图片文件!')
        return false
      }
      if (!isLt2M) {
        ElMessage.error('图片大小不能超过 2MB!')
        return false
      }
      return true
    }

    const handleSuccess = (response) => {
      if (response.success) {
        emit('update:modelValue', response.data.url)
        ElMessage.success('上传成功')
      } else {
        ElMessage.error(response.message || '上传失败')
      }
    }

    const handleError = () => {
      ElMessage.error('上传失败')
    }

    const handleRemove = () => {
      emit('update:modelValue', '')
    }

    return {
      uploadUrl,
      uploadHeaders,
      beforeUpload,
      handleSuccess,
      handleError,
      handleRemove
    }
  }
}
</script>

<style scoped>
.uploader {
  width: 100%;
}

.upload-placeholder {
  width: 200px;
  height: 150px;
  border: 2px dashed #d9d9d9;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: border-color 0.3s;
}

.upload-placeholder:hover {
  border-color: #409eff;
}

.upload-placeholder p {
  margin: 8px 0 0 0;
  color: #606266;
  font-size: 14px;
}

.upload-preview {
  position: relative;
  width: 200px;
  height: 150px;
  border-radius: 6px;
  overflow: hidden;
  cursor: pointer;
}

.upload-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.upload-preview:hover .upload-overlay {
  opacity: 1;
}

.upload-actions {
  margin-top: 8px;
}
</style> 