<template>
  <div class="search-container">
    <el-input
      v-model="searchKeyword"
      placeholder="搜索物品名称、描述或地点..."
      clearable
      @keyup.enter="handleSearch"
      @clear="handleClear"
    >
      <template #prefix>
        <el-icon><Search /></el-icon>
      </template>
      <template #append>
        <el-button @click="handleSearch">
          搜索
        </el-button>
      </template>
    </el-input>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'SearchBar',
  emits: ['search', 'clear'],
  setup(props, { emit }) {
    const searchKeyword = ref('')

    const handleSearch = () => {
      emit('search', searchKeyword.value)
    }

    const handleClear = () => {
      emit('clear')
    }

    return {
      searchKeyword,
      handleSearch,
      handleClear
    }
  }
}
</script>

<style scoped>
.search-container {
  max-width: 600px;
  margin: 0 auto;
}
</style> 