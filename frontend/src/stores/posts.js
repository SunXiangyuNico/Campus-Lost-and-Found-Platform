import { defineStore } from 'pinia'
import { ref } from 'vue'

export const usePostsStore = defineStore('posts', () => {
  const posts = ref([])
  const currentPost = ref(null)
  const myPosts = ref([])
  const claimedPosts = ref([])

  const setPosts = (newPosts) => {
    posts.value = newPosts
  }

  const addPost = (post) => {
    posts.value.unshift(post)
  }

  const setCurrentPost = (post) => {
    currentPost.value = post
  }

  const addMyPost = (post) => {
    myPosts.value.unshift(post)
  }

  const addClaimedPost = (post) => {
    claimedPosts.value.unshift(post)
  }

  const updatePostStatus = (postId, status) => {
    const post = posts.value.find(p => p.id === postId)
    if (post) {
      post.status = status
    }
    
    const myPost = myPosts.value.find(p => p.id === postId)
    if (myPost) {
      myPost.status = status
    }
  }

  return {
    posts,
    currentPost,
    myPosts,
    claimedPosts,
    setPosts,
    addPost,
    setCurrentPost,
    addMyPost,
    addClaimedPost,
    updatePostStatus
  }
}) 