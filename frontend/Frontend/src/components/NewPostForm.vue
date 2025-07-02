<template>
  <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" size="large">
    <el-form-item label="帖子类型" prop="type">
      <el-select v-model="form.type" placeholder="请选择">
        <el-option label="捡到物品帖" value="found" />
        <el-option label="丢失物品帖" value="lost" />
      </el-select>
    </el-form-item>
    <el-form-item label="物品名称" prop="title">
      <el-input v-model="form.title" placeholder="请输入物品名称" />
    </el-form-item>
    <el-form-item label="物品类别" prop="category">
      <el-select v-model="form.category" placeholder="请选择">
        <el-option label="证件" value="id" />
        <el-option label="电子产品" value="electronics" />
        <el-option label="书籍" value="book" />
        <el-option label="衣物" value="clothes" />
        <el-option label="钥匙" value="key" />
        <el-option label="其他" value="other" />
      </el-select>
    </el-form-item>
    <el-form-item :label="form.type === 'found' ? '捡到时间' : '丢失时间'" prop="date">
      <el-date-picker v-model="form.date" type="date" placeholder="yyyy/mm/dd" style="width: 100%" />
    </el-form-item>
    <el-form-item :label="form.type === 'found' ? '捡到地点' : '丢失地点'" prop="location">
      <div class="map-select-block">
        <div class="map-select-tip">点击地图选择具体位置</div>
        <div class="map-select-img-wrapper" @click="onMapClick($event)">
          <img src="/map.png" class="map-img" ref="mapRef" />
          <div v-if="form.mapCoord" class="map-marker" :style="markerStyle"></div>
        </div>
        <div class="map-coord-tip" v-if="form.mapCoord">已选择位置：X: {{ form.mapCoord[0] }}, Y: {{ form.mapCoord[1] }}</div>
      </div>
    </el-form-item>
    <el-form-item label="物品图片" prop="images">
      <el-upload
        class="upload-demo"
        action="#"
        list-type="picture-card"
        :auto-upload="false"
        :on-change="handleImageChange"
        :file-list="form.images"
        :limit="5"
        multiple
        accept="image/*"
      >
        <el-icon><Plus /></el-icon>
      </el-upload>
    </el-form-item>
    <el-form-item label="物品描述" prop="desc">
      <el-input v-model="form.desc" type="textarea" :rows="3" placeholder="请输入物品描述" />
    </el-form-item>
    <el-form-item label="邮箱" prop="contact">
      <el-input v-model="form.contact" placeholder="请输入邮箱" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit" :loading="loading" style="width:100%">发布</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, reactive, computed, defineEmits } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

const emit = defineEmits(['success'])
const formRef = ref()
const mapRef = ref()
const loading = ref(false)
const form = reactive({
  type: '',
  title: '',
  category: '',
  date: '',
  location: '',
  mapCoord: null, // [x, y]
  images: [],
  desc: '',
  contact: ''
})
const rules = {
  type: [{ required: true, message: '请选择帖子类型', trigger: 'change' }],
  title: [{ required: true, message: '请输入物品名称', trigger: 'blur' }],
  category: [{ required: true, message: '请选择物品类别', trigger: 'change' }],
  date: [{ required: true, message: '请选择时间', trigger: 'change' }],
  mapCoord: [{ required: true, message: '请选择地图位置', trigger: 'change' }],
  desc: [{ required: true, message: '请输入物品描述', trigger: 'blur' }],
  contact: [{ required: true, message: '请输入联系方式', trigger: 'blur' }]
}
const markerStyle = computed(() => {
  if (!form.mapCoord) return {}
  return {
    left: form.mapCoord[0] + 'px',
    top: form.mapCoord[1] + 'px'
  }
})
function onMapClick(e) {
  const rect = mapRef.value.getBoundingClientRect()
  const x = Math.round(e.clientX - rect.left)
  const y = Math.round(e.clientY - rect.top)
  form.mapCoord = [x, y]
}
function handleImageChange(file, fileList) {
  form.images = fileList.slice(0, 5)
}
function onSubmit() {
  formRef.value.validate(valid => {
    if (!valid) return
    loading.value = true
    setTimeout(() => {
      ElMessage.success('发布成功！')
      loading.value = false
      emit('success')
      // 清空表单
      Object.assign(form, { type: '', title: '', category: '', date: '', location: '', mapCoord: null, images: [], desc: '', contact: '' })
    }, 1000)
  })
}
</script>

<style scoped>
.map-select-block {
  width: 100%;
}
.map-select-tip {
  color: #888;
  font-size: 14px;
  margin-bottom: 6px;
}
.map-select-img-wrapper {
  position: relative;
  width: 100%;
  max-width: 420px;
  margin: 0 auto;
  cursor: crosshair;
}
.map-img {
  width: 100%;
  max-width: 420px;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 8px #f0f1f2;
}
.map-marker {
  position: absolute;
  width: 22px;
  height: 22px;
  background: #ff4d4f;
  border: 2.5px solid #fff;
  border-radius: 50%;
  left: 0;
  top: 0;
  transform: translate(-50%, -50%);
  box-shadow: 0 2px 8px #ff4d4f44;
  z-index: 2;
}
.map-coord-tip {
  color: #409eff;
  font-size: 15px;
  margin-top: 6px;
  text-align: center;
}
</style> 