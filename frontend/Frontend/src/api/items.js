// 物品相关API将在后续补充 

// mock实现，返回Promise
export function getMyPosts() {
  return Promise.resolve({
    data: [
      {
        id: 1,
        type: 'lost',
        title: '丢失黑色钱包',
        location: '图书馆二楼自习室',
        time: '2024/1/15',
        nickname: '小明',
        avatar: '',
        desc: '在图书馆二楼自习室丢了一个黑色钱包，内有身份证、学生证和少量现金。如有拾到请联系我，必有重谢！',
        images: [],
        claimed: false,
        comments: [],
        locationText: '图书馆二楼自习室',
        locationCoord: [200, 120]
      },
      {
        id: 2,
        type: 'found',
        title: '捡到蓝色水杯',
        location: '松学楼A座一楼大厅',
        time: '2024/1/15',
        nickname: '小李',
        avatar: '',
        desc: '在松学楼A座一楼大厅捡到一个蓝色水杯，有需要的同学请联系我。',
        images: [],
        claimed: false,
        comments: [],
        locationText: '松学楼A座一楼大厅',
        locationCoord: [350, 180]
      }
    ]
  })
} 