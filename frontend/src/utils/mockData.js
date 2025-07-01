// 模拟数据，用于演示界面效果
export const mockPosts = [
  {
    id: 1,
    type: 'lost',
    title: '丢失黑色钱包',
    description: '在图书馆二楼自习室丢失了一个黑色钱包，内有身份证、学生证和少量现金。如有拾到请联系我，必有重谢！',
    location: '图书馆二楼自习室',
    latitude: 39.9042,
    longitude: 116.4074,
    status: 'open',
    createdAt: '2024-01-15T10:30:00Z',
    author: {
      id: 1,
      nickname: '小明',
      avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
      studentId: '2021001'
    },
    images: [
      'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg'
    ],
    comments: [
      {
        id: 1,
        content: '我好像在哪里见过，让我想想',
        createdAt: '2024-01-15T11:00:00Z',
        author: {
          id: 2,
          nickname: '小红',
          avatar: 'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9cpng.png',
          studentId: '2021002'
        }
      }
    ]
  },
  {
    id: 2,
    type: 'found',
    title: '拾到蓝色水杯',
    description: '在教学楼A座一楼大厅拾到一个蓝色保温水杯，上面有"清华大学"字样。失主请到教学楼A座一楼失物招领处认领。',
    location: '教学楼A座一楼大厅',
    latitude: 39.9042,
    longitude: 116.4074,
    status: 'open',
    createdAt: '2024-01-15T09:15:00Z',
    author: {
      id: 3,
      nickname: '小李',
      avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
      studentId: '2021003'
    },
    images: [
      'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg'
    ],
    comments: []
  },
  {
    id: 3,
    type: 'lost',
    title: '丢失苹果手机',
    description: '在食堂吃饭时不小心把iPhone 13落在桌子上了，手机壳是透明的，屏幕有轻微划痕。如有拾到请联系我！',
    location: '学生食堂一楼',
    latitude: 39.9042,
    longitude: 116.4074,
    status: 'claimed',
    createdAt: '2024-01-14T18:20:00Z',
    author: {
      id: 4,
      nickname: '小王',
      avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
      studentId: '2021004'
    },
    images: [
      'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg'
    ],
    comments: [
      {
        id: 2,
        content: '我已经找到了，谢谢大家！',
        createdAt: '2024-01-14T19:30:00Z',
        author: {
          id: 4,
          nickname: '小王',
          avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
          studentId: '2021004'
        }
      }
    ]
  }
]

export const mockUser = {
  id: 1,
  studentId: '2021001',
  nickname: '小明',
  avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
  contact: '13800138000',
  college: '计算机科学与技术学院'
}

export const mockMyPosts = [
  {
    id: 1,
    type: 'lost',
    title: '丢失黑色钱包',
    status: 'open',
    createdAt: '2024-01-15T10:30:00Z'
  }
]

export const mockClaimedPosts = [
  {
    id: 3,
    type: 'lost',
    title: '丢失苹果手机',
    status: 'claimed',
    claimedAt: '2024-01-14T19:30:00Z',
    author: {
      id: 4,
      nickname: '小王',
      studentId: '2021004'
    }
  }
] 